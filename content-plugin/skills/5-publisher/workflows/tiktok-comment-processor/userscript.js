// TikTok Comment Processor v1.1
// Scans comments on a TikTok video for a keyword, DMs followers the Skool link,
// and replies publicly to non-followers asking them to follow + DM.
// Supports two modes:
//   1. Single video mode — pass a video URL, configure keyword in UI
//   2. Profile mode — pass a profile URL, auto-iterates all videos newest-first,
//      auto-detects the keyword per video from the most common comment
// Injected via Playwright addInitScript.

(function () {
    'use strict';

    /*******************************
     *  CONFIG - edit these values *
     *******************************/
    const CONFIG = {
        keyword: 'LINK',
        // DM message for followers
        msgFollower: 'Hey! Here\'s the link to our {YOUR_FREE_COMMUNITY} community: https://{YOUR_COMMUNITY_URL} — see you inside!',
        // Public reply variations for non-followers (up to 3)
        msgsNonFollower: [
            'Hey! Follow me and shoot me a DM and I\'ll send you the link!',
            'Appreciate the interest! Give me a follow and DM me — I\'ll send it right over!',
            'Follow me and send me a quick DM — I\'ll get the link to you!',
        ],
        // Follow-up comment after successful DM (up to 3)
        msgsAfterDM: ['Sent!', 'Just sent it!', 'Check your DMs!'],
        enableMsgAfterDM: true,
        followUpTags: [],
        maxCommentsToProcess: 200,
        perActionDelayMs: [1500, 4000],
        typingDelayMsPerChar: [10, 25],
        replyIntervalMs: [15000, 35000],
        maxRepliesPerSession: 100,
        maxRepliesPerHour: 50,
        sessionCooldownAfter: 15,
        sessionCooldownMs: [60000, 120000],
        likeBeforeReply: false,
        stopOnError: false,
        debugMode: false,
        // Profile mode settings
        autoDetectKeyword: true,      // Auto-detect keyword from most common comment
        minKeywordOccurrences: 3,     // Minimum times a word must appear to be considered a keyword
        skipVideosWithNoKeyword: true, // Skip videos where no clear keyword is found
        betweenVideoDelayMs: [3000, 8000], // Delay between processing videos
    };

    // Global processing state
    let isProcessing = false;
    let processingController = null;
    let videoQueue = [];              // Queue of video URLs for profile mode
    let currentVideoIndex = -1;       // Current position in video queue

    /*******************************
     *  ANTI-DETECTION OVERRIDES   *
     *******************************/
    try {
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    } catch (e) { /* already defined */ }

    try {
        // Fake plugins array
        Object.defineProperty(navigator, 'plugins', {
            get: () => {
                const arr = [
                    { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format' },
                    { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: '' },
                    { name: 'Native Client', filename: 'internal-nacl-plugin', description: '' },
                ];
                arr.item = (i) => arr[i] || null;
                arr.namedItem = (name) => arr.find(p => p.name === name) || null;
                arr.refresh = () => {};
                return arr;
            },
        });
    } catch (e) { /* already defined */ }

    try {
        // Fake chrome runtime
        if (!window.chrome) window.chrome = {};
        if (!window.chrome.runtime) window.chrome.runtime = { id: undefined };
    } catch (e) { /* ignore */ }

    /*******************************
     *  UTILITIES                   *
     *******************************/
    function sleep(ms) {
        return new Promise(r => setTimeout(r, ms));
    }

    function randBetween(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function randDelay(range) {
        return sleep(randBetween(range[0], range[1]));
    }

    function pickRandom(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }

    /**
     * Try multiple selectors and return the first match.
     * Critical for TikTok's CSS-module hashed classes which change between deploys.
     */
    function safeQuery(parent, selectors) {
        if (!parent) return null;
        if (typeof selectors === 'string') selectors = [selectors];
        for (const sel of selectors) {
            try {
                const el = parent.querySelector(sel);
                if (el) return el;
            } catch (e) {
                // Invalid selector, skip
            }
        }
        return null;
    }

    function safeQueryAll(parent, selectors) {
        if (!parent) return [];
        if (typeof selectors === 'string') selectors = [selectors];
        for (const sel of selectors) {
            try {
                const els = parent.querySelectorAll(sel);
                if (els.length > 0) return Array.from(els);
            } catch (e) {
                // Invalid selector, skip
            }
        }
        return [];
    }

    /*******************************
     *  ACTIVITY LOG (DEV LOG)     *
     *******************************/
    const LS_PREFIX = 'tiktok_cp_';
    let _devLogPanel = null;
    const _devLogEntries = [];

    function devLog(text, level = 'info') {
        const time = new Date().toLocaleTimeString();
        const entry = { time, text, level };
        _devLogEntries.push(entry);
        if (CONFIG.debugMode) console.log(`[TT-CP][${level}] ${text}`);

        if (_devLogPanel) {
            const line = document.createElement('div');
            line.style.cssText = `
                padding: 2px 0;
                border-bottom: 1px solid #1a1a2e;
                font-size: 11px;
                line-height: 1.4;
                word-break: break-word;
                color: ${level === 'action' ? '#4ade80' : level === 'error' ? '#f87171' : level === 'warn' ? '#fbbf24' : '#94a3b8'};
            `;
            line.textContent = `${time} ${text}`;
            _devLogPanel.appendChild(line);
            _devLogPanel.scrollTop = _devLogPanel.scrollHeight;
        }
    }

    /*******************************
     *  RATE LIMITER               *
     *******************************/
    const replyTimestamps = [];
    let sessionReplyCount = 0;
    let cooldownActive = false;

    function getRateLimitStatus() {
        const now = Date.now();
        const oneHourAgo = now - 3600000;
        const hourlyCount = replyTimestamps.filter(t => t > oneHourAgo).length;
        const sessionCount = sessionReplyCount;
        const lastReply = replyTimestamps.length > 0 ? replyTimestamps[replyTimestamps.length - 1] : 0;
        const minInterval = CONFIG.replyIntervalMs[0];
        const nextAllowed = lastReply > 0 ? Math.max(0, (lastReply + minInterval) - now) : 0;

        return {
            session: sessionCount,
            maxSession: CONFIG.maxRepliesPerSession,
            hourly: hourlyCount,
            maxHourly: CONFIG.maxRepliesPerHour,
            nextInMs: nextAllowed,
            cooldownActive,
        };
    }

    function canReply() {
        const status = getRateLimitStatus();
        if (status.session >= status.maxSession) return { allowed: false, reason: 'Session limit reached' };
        if (status.hourly >= status.maxHourly) return { allowed: false, reason: 'Hourly limit reached' };
        if (status.nextInMs > 0) return { allowed: false, reason: `Wait ${Math.ceil(status.nextInMs / 1000)}s` };
        if (status.cooldownActive) return { allowed: false, reason: 'Cooldown active' };
        return { allowed: true };
    }

    async function recordReply() {
        replyTimestamps.push(Date.now());
        sessionReplyCount++;

        // Check if cooldown needed
        if (sessionReplyCount > 0 && sessionReplyCount % CONFIG.sessionCooldownAfter === 0) {
            cooldownActive = true;
            const cooldownMs = randBetween(CONFIG.sessionCooldownMs[0], CONFIG.sessionCooldownMs[1]);
            devLog(`Cooldown: pausing ${Math.round(cooldownMs / 1000)}s after ${sessionReplyCount} replies`, 'warn');
            updateRateLimitDisplay();
            await sleep(cooldownMs);
            cooldownActive = false;
            devLog('Cooldown complete, resuming', 'info');
        }
    }

    async function waitForRateLimit() {
        let check = canReply();
        while (!check.allowed) {
            devLog(`Rate limit: ${check.reason}`, 'warn');
            updateRateLimitDisplay();
            await sleep(5000);
            check = canReply();
        }
        // Wait the required interval between replies
        const status = getRateLimitStatus();
        if (status.nextInMs > 0) {
            await sleep(status.nextInMs);
        }
        // Add random jitter
        await randDelay(CONFIG.replyIntervalMs);
    }

    /*******************************
     *  LOCALSTORAGE HELPERS       *
     *******************************/
    function lsGet(key, fallback = null) {
        try {
            const raw = localStorage.getItem(LS_PREFIX + key);
            return raw ? JSON.parse(raw) : fallback;
        } catch { return fallback; }
    }

    function lsSet(key, value) {
        try {
            localStorage.setItem(LS_PREFIX + key, JSON.stringify(value));
        } catch (e) {
            devLog(`localStorage write error: ${e}`, 'error');
        }
    }

    function lsRemove(key) {
        try { localStorage.removeItem(LS_PREFIX + key); } catch {}
    }

    /*******************************
     *  SETTINGS PERSISTENCE       *
     *******************************/
    function saveSettings() {
        lsSet('settings', {
            keyword: CONFIG.keyword,
            msgFollower: CONFIG.msgFollower,
            msgsNonFollower: CONFIG.msgsNonFollower,
            msgsAfterDM: CONFIG.msgsAfterDM,
            enableMsgAfterDM: CONFIG.enableMsgAfterDM,
            followUpTags: CONFIG.followUpTags,
            likeBeforeReply: CONFIG.likeBeforeReply,
        });
        devLog('Settings saved to localStorage', 'action');
    }

    function loadSettings() {
        const saved = lsGet('settings');
        if (!saved) return;
        if (saved.keyword !== undefined) CONFIG.keyword = saved.keyword;
        if (saved.msgFollower !== undefined) CONFIG.msgFollower = saved.msgFollower;
        if (saved.msgsNonFollower !== undefined) CONFIG.msgsNonFollower = saved.msgsNonFollower;
        if (saved.msgsAfterDM !== undefined) CONFIG.msgsAfterDM = saved.msgsAfterDM;
        if (saved.enableMsgAfterDM !== undefined) CONFIG.enableMsgAfterDM = saved.enableMsgAfterDM;
        if (saved.followUpTags !== undefined) CONFIG.followUpTags = saved.followUpTags;
        if (saved.likeBeforeReply !== undefined) CONFIG.likeBeforeReply = saved.likeBeforeReply;
        devLog('Settings loaded from localStorage', 'info');
    }

    /*******************************
     *  CURRENT USER DETECTION     *
     *******************************/
    let _currentUsername = null;

    function getCurrentUsername() {
        if (_currentUsername) return _currentUsername;

        // Try profile link in nav/header
        const profileLink = safeQuery(document, [
            'a[data-e2e="nav-profile"]',
            'a[href*="/@"][data-e2e]',
            'div[data-e2e="profile-icon"] a',
        ]);
        if (profileLink) {
            const href = profileLink.getAttribute('href') || '';
            const match = href.match(/\/@([^/?]+)/);
            if (match) {
                _currentUsername = match[1];
                devLog(`Current user detected: @${_currentUsername}`, 'info');
                return _currentUsername;
            }
        }

        // Try from unique-id in page metadata
        const metaEl = safeQuery(document, ['meta[property="og:url"]']);
        if (metaEl) {
            const content = metaEl.getAttribute('content') || '';
            const match = content.match(/\/@([^/?]+)/);
            if (match) {
                _currentUsername = match[1];
                devLog(`Current user detected from meta: @${_currentUsername}`, 'info');
                return _currentUsername;
            }
        }

        return null;
    }

    /*******************************
     *  PAGE DETECTION             *
     *******************************/
    function isVideoPage() {
        return /\/@[^/]+\/video\/\d+/.test(window.location.pathname);
    }

    function isProfilePage() {
        return /^\/@[^/]+\/?$/.test(window.location.pathname);
    }

    /*******************************
     *  PROFILE MODE — VIDEO GRID  *
     *******************************/

    /**
     * Scroll the profile video grid to load all videos.
     * Returns an array of video URLs (newest first — TikTok default order).
     */
    async function scrapeProfileVideos() {
        devLog('Scraping video grid from profile...', 'info');

        const videoSelectors = [
            'div[data-e2e="user-post-item"] a',
            'div[data-e2e="user-post-item-list"] a[href*="/video/"]',
            'div[class*="DivItemContainerV2"] a[href*="/video/"]',
            'div[class*="DivVideoFeed"] a[href*="/video/"]',
            'a[href*="/video/"]',
        ];

        let previousCount = 0;
        let noGrowthAttempts = 0;
        const maxNoGrowth = 3;

        while (noGrowthAttempts < maxNoGrowth) {
            let videoLinks = [];
            for (const sel of videoSelectors) {
                try {
                    const links = document.querySelectorAll(sel);
                    if (links.length > 0) {
                        videoLinks = Array.from(links);
                        break;
                    }
                } catch (e) {}
            }

            const currentCount = videoLinks.length;

            if (currentCount > previousCount) {
                noGrowthAttempts = 0;
                previousCount = currentCount;
                devLog(`Found ${currentCount} videos so far...`, 'info');
            } else {
                noGrowthAttempts++;
            }

            // Scroll page down to load more
            window.scrollTo(0, document.body.scrollHeight);
            await sleep(randBetween(1000, 2000));
        }

        // Collect final set of video URLs
        let allLinks = [];
        for (const sel of videoSelectors) {
            try {
                const links = document.querySelectorAll(sel);
                if (links.length > 0) {
                    allLinks = Array.from(links);
                    break;
                }
            } catch (e) {}
        }

        const urls = [];
        const seen = new Set();
        for (const link of allLinks) {
            const href = link.getAttribute('href');
            if (!href || !href.includes('/video/')) continue;
            const fullUrl = href.startsWith('http') ? href : `https://www.tiktok.com${href}`;
            if (!seen.has(fullUrl)) {
                seen.add(fullUrl);
                urls.push(fullUrl);
            }
        }

        devLog(`Profile scrape complete: ${urls.length} videos found`, 'action');
        return urls; // Already newest-first (TikTok default grid order)
    }

    /**
     * Auto-detect the keyword for a video by finding the most common comment.
     * Looks for single-word or short comments that appear many times — these are
     * the CTA keyword comments (e.g. "LINK", "AGENT", "YES").
     */
    function autoDetectKeyword(comments) {
        // Common words to ignore
        const ignoreWords = new Set([
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'shall', 'can', 'to', 'of', 'in', 'for',
            'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over',
            'under', 'again', 'further', 'then', 'once', 'and', 'but', 'or', 'nor',
            'not', 'so', 'yet', 'both', 'either', 'neither', 'each', 'every', 'all',
            'any', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'only',
            'own', 'same', 'than', 'too', 'very', 'just', 'because', 'if', 'when',
            'where', 'how', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
            'those', 'i', 'me', 'my', 'you', 'your', 'he', 'she', 'it', 'we', 'they',
            'them', 'his', 'her', 'its', 'our', 'their', 'lol', 'lmao', 'omg', 'wow',
            'like', 'love', 'great', 'good', 'nice', 'cool', 'amazing', 'awesome',
            'thanks', 'thank', 'please', 'yes', 'no', 'ok', 'okay',
        ]);

        // Count frequency of trimmed, lowercased comment texts
        const freq = {};
        for (const comment of comments) {
            const text = comment.text.trim().toLowerCase();
            // Only consider short comments (1-3 words) as potential keywords
            const wordCount = text.split(/\s+/).length;
            if (wordCount > 3 || text.length === 0) continue;
            if (wordCount === 1 && ignoreWords.has(text)) continue;

            freq[text] = (freq[text] || 0) + 1;
        }

        // Find the most common short comment
        let bestKeyword = null;
        let bestCount = 0;
        for (const [text, count] of Object.entries(freq)) {
            if (count > bestCount && count >= CONFIG.minKeywordOccurrences) {
                bestCount = count;
                bestKeyword = text;
            }
        }

        if (bestKeyword) {
            devLog(`Auto-detected keyword: "${bestKeyword}" (${bestCount} occurrences)`, 'action');
        } else {
            devLog('Could not auto-detect keyword — no short comment appears frequently enough', 'warn');
        }

        return bestKeyword;
    }

    /**
     * Profile mode: process all videos sequentially.
     * Saves queue to localStorage so navigation between pages continues the flow.
     */
    async function startProfileMode(videoUrls) {
        if (videoUrls.length === 0) {
            devLog('No videos to process', 'warn');
            return;
        }

        // Save queue to localStorage
        lsSet('videoQueue', videoUrls);
        lsSet('videoQueueIndex', 0);
        lsSet('profileModeActive', true);
        lsSet('profileModeStats', { processed: 0, skipped: 0, total: videoUrls.length });

        devLog(`Profile mode: queued ${videoUrls.length} videos. Navigating to first video...`, 'action');
        await sleep(randBetween(2000, 4000));

        // Navigate to first video
        window.location.href = videoUrls[0];
    }

    /**
     * Continue profile mode: called on video pages when a queue exists.
     * Auto-detects keyword, processes, then navigates to next video.
     */
    async function continueProfileMode() {
        const queue = lsGet('videoQueue', []);
        const index = lsGet('videoQueueIndex', 0);
        const stats = lsGet('profileModeStats', { processed: 0, skipped: 0, total: 0 });

        if (index >= queue.length) {
            devLog(`\n=== PROFILE MODE COMPLETE ===`, 'action');
            devLog(`Processed: ${stats.processed} | Skipped: ${stats.skipped} | Total: ${stats.total}`, 'action');
            lsRemove('videoQueue');
            lsRemove('videoQueueIndex');
            lsRemove('profileModeActive');
            lsRemove('profileModeStats');
            return;
        }

        devLog(`\n=== Video ${index + 1}/${queue.length}: ${queue[index]} ===`, 'action');

        // Wait for page and comments to load
        devLog('Waiting for video page to load...', 'info');
        await sleep(3000);

        // Scroll and load comments (includes ensureCommentsVisible)
        await autoScrollComments();

        // Extract all comments for keyword detection
        const commentItems = findCommentItemsGlobal();
        const allComments = commentItems.map(el => extractCommentData(el)).filter(c => c.text);

        if (allComments.length === 0) {
            devLog('No comments found on this video — skipping', 'warn');
            stats.skipped++;
            lsSet('profileModeStats', stats);
            await navigateToNextVideo(queue, index);
            return;
        }

        // Auto-detect keyword
        let keyword = CONFIG.autoDetectKeyword ? autoDetectKeyword(allComments) : CONFIG.keyword;

        if (!keyword) {
            if (CONFIG.skipVideosWithNoKeyword) {
                devLog('No keyword detected — skipping this video', 'warn');
                stats.skipped++;
                lsSet('profileModeStats', stats);
                await navigateToNextVideo(queue, index);
                return;
            }
            keyword = CONFIG.keyword; // Fallback to configured keyword
        }

        // Override CONFIG keyword for this video
        CONFIG.keyword = keyword.toUpperCase();
        devLog(`Using keyword: "${CONFIG.keyword}" for this video`, 'info');

        // Run the processor
        await runProcessor();

        stats.processed++;
        lsSet('profileModeStats', stats);

        await navigateToNextVideo(queue, index);
    }

    async function navigateToNextVideo(queue, currentIndex) {
        const nextIndex = currentIndex + 1;
        lsSet('videoQueueIndex', nextIndex);

        if (nextIndex >= queue.length) {
            const stats = lsGet('profileModeStats', { processed: 0, skipped: 0, total: 0 });
            devLog(`\n=== PROFILE MODE COMPLETE ===`, 'action');
            devLog(`Processed: ${stats.processed} | Skipped: ${stats.skipped} | Total: ${stats.total}`, 'action');
            lsRemove('videoQueue');
            lsRemove('videoQueueIndex');
            lsRemove('profileModeActive');
            lsRemove('profileModeStats');
            return;
        }

        const delay = randBetween(CONFIG.betweenVideoDelayMs[0], CONFIG.betweenVideoDelayMs[1]);
        devLog(`Moving to next video in ${Math.round(delay / 1000)}s... (${nextIndex + 1}/${queue.length})`, 'info');
        await sleep(delay);

        window.location.href = queue[nextIndex];
    }

    /*******************************
     *  TEXT INSERTION             *
     *******************************/
    async function insertText(element, text) {
        element.focus();
        await sleep(200);

        // Method 1: execCommand('insertText')
        const success = document.execCommand('insertText', false, text);
        if (success && element.textContent.includes(text)) {
            devLog('Text inserted via execCommand', 'info');
            return true;
        }

        // Method 2: Clipboard paste simulation
        try {
            element.focus();
            const dataTransfer = new DataTransfer();
            dataTransfer.setData('text/plain', text);
            const pasteEvent = new ClipboardEvent('paste', {
                bubbles: true,
                cancelable: true,
                clipboardData: dataTransfer,
            });
            element.dispatchEvent(pasteEvent);
            await sleep(200);
            if (element.textContent.includes(text)) {
                devLog('Text inserted via paste simulation', 'info');
                return true;
            }
        } catch (e) {
            devLog(`Paste simulation failed: ${e}`, 'warn');
        }

        // Method 3: Direct value set with input events
        try {
            element.textContent = text;
            element.dispatchEvent(new Event('input', { bubbles: true }));
            element.dispatchEvent(new Event('change', { bubbles: true }));
            await sleep(200);
            if (element.textContent.includes(text)) {
                devLog('Text inserted via direct set + input event', 'info');
                return true;
            }
        } catch (e) {
            devLog(`Direct set failed: ${e}`, 'warn');
        }

        devLog('All text insertion methods failed', 'error');
        return false;
    }

    /**
     * Type text character by character with human-like delays.
     */
    async function typeText(element, text) {
        element.focus();
        await sleep(200);

        for (const char of text) {
            document.execCommand('insertText', false, char);
            await sleep(randBetween(CONFIG.typingDelayMsPerChar[0], CONFIG.typingDelayMsPerChar[1]));
        }

        await sleep(300);
        if (element.textContent.includes(text)) {
            devLog('Text typed character by character', 'info');
            return true;
        }

        // Fallback to bulk insert
        return insertText(element, text);
    }

    /*******************************
     *  COMMENT DISCOVERY          *
     *******************************/
    const SELECTORS = {
        commentList: [
            'div[data-e2e="comment-list"]',
            'div[class*="DivCommentListContainer"]',
            'div[class*="DivCommentContainer"]',
            'div[class*="CommentList"]',
        ],
        commentItem: [
            'div[data-e2e="comment-item"]',
            'div[class*="DivCommentItemContainer"]',
            'div[class*="DivCommentObjectWrapper"]',
            'div[class*="CommentItem"]',
        ],
        commentText: [
            'span[data-e2e="comment-level-1"]',
            'p[data-e2e="comment-level-1"]',
            'p[class*="PCommentText"]',
            'span[data-e2e="comment-text"]',
            'span[class*="SpanCommentText"]',
        ],
        username: [
            'a[data-e2e="comment-username-1"]',
            'a[data-e2e="comment-username"]',
            'span[class*="SpanUserNameText"]',
            'a[class*="StyledLink"][href*="/@"]',
        ],
        authorBadge: ['span[data-e2e="comment-author-tag"]', 'span[class*="SpanAuthorTag"]', 'div[class*="DivBadge"]'],
        replyButton: ['span[data-e2e="comment-reply-1"]', 'p[class*="PReplyLabel"]', 'span[data-e2e="comment-reply"]', 'span[data-e2e="comment-reply-icon"]'],
        replyInput: [
            'div[data-e2e="comment-input"] div[contenteditable="true"]',
            'div[class*="DivInputEditorContainer"] div[contenteditable="true"]',
            'div[contenteditable="true"][data-e2e="comment-text-area"]',
        ],
        replySubmit: ['div[data-e2e="comment-post"]', 'button[data-e2e="comment-post"]', 'div[class*="DivPostButton"]'],
        likeButton: ['span[data-e2e="comment-like-icon"]', 'div[class*="DivLikeWrapper"] span'],
        replyList: ['div[data-e2e="comment-reply-list"]', 'div[class*="DivReplyContainer"]'],
        replyItem: ['div[data-e2e="comment-reply-item"]', 'div[class*="DivCommentReplyItem"]'],
        viewRepliesButton: ['span[data-e2e="view-more-replies"]', 'p[class*="PReplyAction"]'],
        // Profile page selectors
        followButton: ['button[data-e2e="follow-button"]', 'button[class*="ButtonFollow"]'],
        followBackButton: ['button[data-e2e="follow-back-button"]', 'button[class*="ButtonFollowBack"]'],
        friendsButton: ['button[data-e2e="friends-button"]', 'button[class*="ButtonFriends"]'],
        // DM selectors
        dmButton: ['a[data-e2e="message-icon"]', 'button[data-e2e="profile-message"]', 'div[class*="DivMessageIcon"] a'],
        chatComposer: [
            'div[class*="DivEditorContainer"] div[contenteditable="true"]',
            'div[data-e2e="message-input"] div[contenteditable="true"]',
            'div[contenteditable="true"][data-e2e="chat-input"]',
        ],
        sendButton: ['button[data-e2e="message-send"]', 'div[class*="DivSendButton"]', 'button[class*="ButtonSend"]'],
    };

    /**
     * Try to open the comment panel if it's not already visible.
     * On desktop TikTok, comments are usually in the right panel on video pages,
     * but sometimes need to be triggered by clicking the comment icon.
     */
    async function ensureCommentsVisible() {
        // Check if comments are already visible
        let commentList = safeQuery(document, SELECTORS.commentList);
        if (commentList && commentList.children.length > 0) {
            devLog('Comment panel already visible', 'info');
            return true;
        }

        // Debug: log what data-e2e elements exist on the page
        const allE2E = document.querySelectorAll('[data-e2e]');
        const e2eValues = new Set();
        allE2E.forEach(el => e2eValues.add(el.getAttribute('data-e2e')));
        devLog(`Found ${allE2E.length} data-e2e elements: ${Array.from(e2eValues).join(', ')}`, 'info');

        // Try clicking the comment icon to open the panel
        const commentIconSelectors = [
            'button[data-e2e="comment-icon"]',
            'span[data-e2e="comment-icon"]',
            'div[data-e2e="comment-icon"]',
            '[data-e2e="browse-comment-icon"]',
            '[data-e2e="comment-count"]',
            // Broader fallbacks — look for comment-related buttons
            'button[class*="Comment"]',
            'div[class*="DivCommentIcon"]',
        ];

        for (const sel of commentIconSelectors) {
            try {
                const icon = document.querySelector(sel);
                if (icon) {
                    devLog(`Clicking comment icon: ${sel}`, 'info');
                    icon.click();
                    await sleep(3000);

                    commentList = safeQuery(document, SELECTORS.commentList);
                    if (commentList) {
                        devLog('Comment panel opened after clicking icon', 'action');
                        return true;
                    }
                }
            } catch (e) {}
        }

        // Try broader search: any scrollable container with multiple similar child divs
        // that looks like a comment list
        const broadSelectors = [
            // TikTok 2024-2026 desktop layouts
            'div[class*="comment" i]',
            'div[class*="Comment"]',
            'div[data-e2e*="comment"]',
            // The main content area beside the video
            'div[class*="DivContentContainer"]',
            'div[class*="DivCommentContainer"]',
        ];

        for (const sel of broadSelectors) {
            try {
                const els = document.querySelectorAll(sel);
                for (const el of els) {
                    if (el.children.length >= 2 && el.scrollHeight > el.clientHeight) {
                        devLog(`Found potential comment container via broad search: ${sel} (${el.children.length} children, scrollable)`, 'info');
                        // Update SELECTORS dynamically
                        SELECTORS.commentList.unshift(sel);
                        return true;
                    }
                }
            } catch (e) {}
        }

        devLog('Could not find or open comment panel', 'warn');
        return false;
    }

    /**
     * Scroll the comment panel to load more comments.
     * TikTok uses infinite scroll in the comment side panel.
     */
    async function autoScrollComments() {
        devLog('Starting comment scroll...', 'info');

        // First ensure the comment panel is open
        await ensureCommentsVisible();

        let commentList = safeQuery(document, SELECTORS.commentList);
        if (!commentList) {
            // Last resort: try to find any container with comment-like content
            devLog('Comment list container not found — trying broad DOM scan...', 'warn');

            // Look for elements containing typical comment patterns (usernames, timestamps)
            const allDivs = document.querySelectorAll('div');
            for (const div of allDivs) {
                const links = div.querySelectorAll('a[href*="/@"]');
                if (links.length >= 3 && div.scrollHeight > 200) {
                    devLog(`Found likely comment container: ${div.className.substring(0, 60)} (${links.length} profile links)`, 'info');
                    // Use this as the comment list
                    div.dataset.e2e = 'comment-list';
                    break;
                }
            }

            commentList = safeQuery(document, SELECTORS.commentList);
            if (!commentList) {
                devLog('Comment list container not found after all attempts', 'error');
                return 0;
            }
        }

        // Debug: dump the structure of the comment list so we know what selectors to use
        if (commentList) {
            const children = Array.from(commentList.children);
            devLog(`Comment list has ${children.length} direct children`, 'info');
            for (let i = 0; i < Math.min(3, children.length); i++) {
                const child = children[i];
                const tag = child.tagName.toLowerCase();
                const cls = child.className ? child.className.substring(0, 80) : '(no class)';
                const e2e = child.getAttribute('data-e2e') || '(no data-e2e)';
                const innerE2Es = Array.from(child.querySelectorAll('[data-e2e]')).map(el => el.getAttribute('data-e2e')).join(', ');
                devLog(`  child[${i}]: <${tag}> class="${cls}" data-e2e="${e2e}" inner-e2e=[${innerE2Es}]`, 'info');
                // Also dump the first link
                const link = child.querySelector('a[href*="/@"]');
                if (link) devLog(`    first link: ${link.getAttribute('href')} text="${link.textContent.trim().substring(0, 30)}"`, 'info');
                // And any text content that looks like a comment
                const textEls = child.querySelectorAll('p, span');
                for (const t of Array.from(textEls).slice(0, 3)) {
                    const txt = t.textContent.trim();
                    if (txt.length > 2 && txt.length < 200) {
                        devLog(`    text: <${t.tagName.toLowerCase()} class="${(t.className || '').substring(0, 40)}" e2e="${t.getAttribute('data-e2e') || ''}"> "${txt.substring(0, 60)}"`, 'info');
                    }
                }
            }
        }

        // Try to find comment items, with fallback to direct children
        let findCommentItems = () => {
            let items = safeQueryAll(commentList, SELECTORS.commentItem);
            if (items.length > 0) return items;

            // Fallback: direct children of the comment list that contain profile links
            items = Array.from(commentList.children).filter(child => {
                return child.querySelector('a[href*="/@"]') !== null;
            });
            if (items.length > 0) {
                devLog(`Using fallback: ${items.length} direct children with profile links as comment items`, 'info');
            }
            return items;
        };

        let previousCount = 0;
        let noGrowthAttempts = 0;
        const maxNoGrowth = 3;

        while (noGrowthAttempts < maxNoGrowth) {
            const items = findCommentItems();
            const currentCount = items.length;

            if (currentCount > previousCount) {
                noGrowthAttempts = 0;
                previousCount = currentCount;
                devLog(`Loaded ${currentCount} comments so far...`, 'info');
            } else {
                noGrowthAttempts++;
                devLog(`No new comments (attempt ${noGrowthAttempts}/${maxNoGrowth})`, 'info');
            }

            if (currentCount >= CONFIG.maxCommentsToProcess) {
                devLog(`Reached max comments limit (${CONFIG.maxCommentsToProcess})`, 'info');
                break;
            }

            // Scroll the comment panel down
            commentList.scrollTop = commentList.scrollHeight;
            await sleep(randBetween(1000, 2000));
        }

        const finalCount = findCommentItems().length;
        devLog(`Comment scroll complete: ${finalCount} comments loaded`, 'action');
        return finalCount;
    }

    /**
     * Find comment items using standard selectors with fallback to profile-link children.
     */
    function findCommentItemsGlobal() {
        const commentList = safeQuery(document, SELECTORS.commentList);
        if (!commentList) return [];

        let items = safeQueryAll(commentList, SELECTORS.commentItem);
        if (items.length > 0) return items;

        // Fallback: direct children containing profile links
        return Array.from(commentList.children).filter(child =>
            child.querySelector('a[href*="/@"]') !== null
        );
    }

    /**
     * Extract comment data from a comment element.
     * Tries standard selectors first, then falls back to scanning for text/links.
     */
    function extractCommentData(commentEl) {
        let textEl = safeQuery(commentEl, SELECTORS.commentText);
        let usernameEl = safeQuery(commentEl, SELECTORS.username);
        const authorBadgeEl = safeQuery(commentEl, SELECTORS.authorBadge);

        // Fallback: find username from any anchor with /@username href
        if (!usernameEl) {
            const links = commentEl.querySelectorAll('a[href*="/@"]');
            if (links.length > 0) usernameEl = links[0];
        }

        // Fallback: find comment text from any <p> or <span> that isn't the username
        if (!textEl) {
            const candidates = commentEl.querySelectorAll('p, span');
            for (const el of candidates) {
                const txt = el.textContent.trim();
                // Skip very short text (timestamps, numbers), skip username text
                if (txt.length < 1 || txt.length > 500) continue;
                if (el.closest('a[href*="/@"]')) continue; // Skip username links
                if (/^\d+[smhd]?\s*(ago)?$/i.test(txt)) continue; // Skip timestamps like "2h ago"
                if (/^\d+$/.test(txt)) continue; // Skip pure numbers (like counts)
                if (/^(Reply|View|Like|Share)$/i.test(txt)) continue; // Skip action labels
                textEl = el;
                break;
            }
        }

        const text = textEl ? textEl.textContent.trim() : '';
        let username = '';
        let profileUrl = '';

        if (usernameEl) {
            // Username might be in an anchor tag with href
            const anchor = usernameEl.tagName === 'A' ? usernameEl : usernameEl.closest('a');
            if (anchor) {
                const href = anchor.getAttribute('href') || '';
                const match = href.match(/\/@([^/?]+)/);
                if (match) username = match[1];
                profileUrl = href.startsWith('/') ? `https://www.tiktok.com${href}` : href;
            }
            if (!username) {
                username = usernameEl.textContent.trim().replace(/^@/, '');
            }
            if (!profileUrl && username) {
                profileUrl = `https://www.tiktok.com/@${username}`;
            }
        }

        const isAuthor = !!authorBadgeEl;

        return { text, username, profileUrl, isAuthor, element: commentEl };
    }

    /**
     * Check if a comment thread has an existing reply from us.
     * Returns { handled: boolean, hasNonFollowerReply: boolean }
     */
    function checkExistingReplies(commentEl) {
        const currentUser = getCurrentUsername();
        if (!currentUser) return { handled: false, hasNonFollowerReply: false };

        // Look for reply list under this comment
        const replyContainer = safeQuery(commentEl, SELECTORS.replyList) ||
            commentEl.nextElementSibling;

        if (!replyContainer) return { handled: false, hasNonFollowerReply: false };

        const replies = safeQueryAll(replyContainer, SELECTORS.replyItem);
        let hasNonFollowerReply = false;

        for (const reply of replies) {
            const replyData = extractCommentData(reply);
            if (replyData.username.toLowerCase() !== currentUser.toLowerCase()) continue;

            const replyText = replyData.text.toLowerCase();

            // Check against all skip patterns
            const allSkipPatterns = [
                ...CONFIG.msgsNonFollower,
                ...CONFIG.msgsAfterDM,
                ...CONFIG.followUpTags,
            ];

            for (const pattern of allSkipPatterns) {
                if (replyText.includes(pattern.toLowerCase())) {
                    // Determine if it was a non-follower reply
                    for (const nfMsg of CONFIG.msgsNonFollower) {
                        if (replyText.includes(nfMsg.toLowerCase())) {
                            hasNonFollowerReply = true;
                        }
                    }
                    return { handled: true, hasNonFollowerReply };
                }
            }
        }

        return { handled: false, hasNonFollowerReply: false };
    }

    /**
     * Analyze comments and return keyword matches.
     */
    async function analyzeComments() {
        devLog('Analyzing comments...', 'info');

        const commentItems = findCommentItemsGlobal();
        if (commentItems.length === 0) {
            devLog('No comment items found', 'error');
            return [];
        }
        devLog(`Found ${commentItems.length} comment items to analyze`, 'info');
        const keyword = CONFIG.keyword.toLowerCase();
        const matches = [];

        for (const item of commentItems) {
            const data = extractCommentData(item);
            if (!data.text || !data.username) continue;

            // Check keyword match
            if (!data.text.toLowerCase().includes(keyword)) continue;

            // Skip video author
            if (data.isAuthor) {
                devLog(`Skipping author comment: @${data.username}`, 'info');
                continue;
            }

            // Skip self
            const currentUser = getCurrentUsername();
            if (currentUser && data.username.toLowerCase() === currentUser.toLowerCase()) continue;

            // Check existing replies
            const { handled, hasNonFollowerReply } = checkExistingReplies(item);
            if (handled && !hasNonFollowerReply) {
                devLog(`Skipping @${data.username} — already handled`, 'warn');
                continue;
            }

            matches.push({
                ...data,
                hasNonFollowerReply,
                needsReprocess: hasNonFollowerReply, // Was non-follower, might now be follower
            });
        }

        devLog(`Found ${matches.length} keyword matches out of ${commentItems.length} comments`, 'action');
        return matches;
    }

    /*******************************
     *  FOLLOWER DETECTION         *
     *******************************/

    /**
     * Check if a user follows us by opening their profile in a new tab.
     * Returns: { isFollower: boolean, isMutual: boolean }
     */
    async function checkFollowerStatus(username, profileUrl) {
        devLog(`Checking follower status for @${username}...`, 'info');

        // Write the check task to localStorage
        lsSet('followCheck', { username, profileUrl, timestamp: Date.now() });
        lsRemove('followCheckResult');

        // Open profile in new tab
        const profileTab = window.open(profileUrl, '_blank');
        if (!profileTab) {
            devLog(`Failed to open profile tab for @${username}`, 'error');
            return { isFollower: false, isMutual: false };
        }

        // Poll for result
        const maxWait = 12000;
        const pollInterval = 300;
        let elapsed = 0;

        while (elapsed < maxWait) {
            await sleep(pollInterval);
            elapsed += pollInterval;

            const result = lsGet('followCheckResult');
            if (result && result.username === username) {
                devLog(`Follower check result for @${username}: follower=${result.isFollower}, mutual=${result.isMutual}`, 'action');
                lsRemove('followCheckResult');
                try { profileTab.close(); } catch {}
                return { isFollower: result.isFollower, isMutual: result.isMutual };
            }
        }

        devLog(`Follower check timed out for @${username}`, 'warn');
        try { profileTab.close(); } catch {}
        lsRemove('followCheck');
        return { isFollower: false, isMutual: false };
    }

    /**
     * Run on profile pages — detect follow button state and write result.
     * This runs in the profile tab opened by checkFollowerStatus.
     */
    async function handleProfilePage() {
        const task = lsGet('followCheck');
        if (!task) {
            // Check for DM task instead
            await handleDMTask();
            return;
        }

        devLog(`[Profile] Checking follow state for @${task.username}`, 'info');

        // Wait for profile to load
        await sleep(1500);
        let attempts = 0;
        const maxAttempts = 6;

        while (attempts < maxAttempts) {
            // Check for "Follow back" button → they follow us
            const followBack = safeQuery(document, SELECTORS.followBackButton);
            if (followBack && followBack.textContent.toLowerCase().includes('follow back')) {
                lsSet('followCheckResult', {
                    username: task.username,
                    isFollower: true,
                    isMutual: false,
                });
                devLog(`[Profile] @${task.username} follows us (follow back visible)`, 'action');
                return;
            }

            // Check for "Friends" button → mutual
            const friends = safeQuery(document, SELECTORS.friendsButton);
            if (friends && friends.textContent.toLowerCase().includes('friends')) {
                lsSet('followCheckResult', {
                    username: task.username,
                    isFollower: true,
                    isMutual: true,
                });
                devLog(`[Profile] @${task.username} is a mutual follower (friends)`, 'action');
                return;
            }

            // Check for "Follow" button → not following us
            const followBtn = safeQuery(document, SELECTORS.followButton);
            if (followBtn) {
                const btnText = followBtn.textContent.toLowerCase().trim();
                if (btnText === 'follow') {
                    lsSet('followCheckResult', {
                        username: task.username,
                        isFollower: false,
                        isMutual: false,
                    });
                    devLog(`[Profile] @${task.username} does not follow us`, 'info');
                    return;
                }
            }

            // Broad fallback: scan ALL buttons for follow-related text
            const allButtons = document.querySelectorAll('button');
            for (const btn of allButtons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text === 'follow back' || text === 'follow back ') {
                    lsSet('followCheckResult', { username: task.username, isFollower: true, isMutual: false });
                    devLog(`[Profile] @${task.username} follows us (broad scan: "${text}")`, 'action');
                    return;
                }
                if (text === 'friends' || text === 'friends ') {
                    lsSet('followCheckResult', { username: task.username, isFollower: true, isMutual: true });
                    devLog(`[Profile] @${task.username} is mutual (broad scan: "${text}")`, 'action');
                    return;
                }
                if (text === 'follow' && btn.offsetWidth > 50) {
                    lsSet('followCheckResult', { username: task.username, isFollower: false, isMutual: false });
                    devLog(`[Profile] @${task.username} does not follow us (broad scan)`, 'info');
                    return;
                }
            }

            attempts++;
            await sleep(800);
        }

        // Timeout — assume not a follower
        lsSet('followCheckResult', {
            username: task.username,
            isFollower: false,
            isMutual: false,
        });
        devLog(`[Profile] Could not determine follow state for @${task.username}, assuming non-follower`, 'warn');
    }

    /*******************************
     *  DM FLOW (CROSS-TAB)       *
     *******************************/

    /**
     * Send DM via cross-tab coordination.
     * Main tab writes dmTask, opens profile, profile tab sends the DM.
     */
    async function sendDM(username, profileUrl, message) {
        devLog(`Starting DM flow for @${username}...`, 'info');

        // Write the DM task
        lsSet('dmTask', {
            username,
            profileUrl,
            message,
            timestamp: Date.now(),
        });
        lsRemove('dmTaskResult');

        // Open profile in new tab
        const dmTab = window.open(profileUrl, '_blank');
        if (!dmTab) {
            devLog(`Failed to open DM tab for @${username}`, 'error');
            lsRemove('dmTask');
            return false;
        }

        // Poll for result
        const maxWait = 30000;
        const pollInterval = 1000;
        let elapsed = 0;

        while (elapsed < maxWait) {
            await sleep(pollInterval);
            elapsed += pollInterval;

            const result = lsGet('dmTaskResult');
            if (result && result.username === username) {
                // Replay logs
                if (result.logs) {
                    for (const log of result.logs) {
                        devLog(`[DM] ${log.text}`, log.level || 'info');
                    }
                }

                lsRemove('dmTaskResult');
                try { dmTab.close(); } catch {}

                if (result.success) {
                    devLog(`DM sent successfully to @${username}`, 'action');
                    return true;
                } else {
                    devLog(`DM failed for @${username}: ${result.error || 'unknown'}`, 'error');
                    return false;
                }
            }
        }

        devLog(`DM timed out for @${username}`, 'warn');
        try { dmTab.close(); } catch {}
        lsRemove('dmTask');
        return false;
    }

    /**
     * Handle DM task on profile page (runs in the DM tab).
     */
    async function handleDMTask() {
        const task = lsGet('dmTask');
        if (!task) return;

        const logs = [];
        function dmLog(text, level = 'info') {
            logs.push({ text, level });
            if (CONFIG.debugMode) console.log(`[TT-CP-DM][${level}] ${text}`);
        }

        dmLog(`Starting DM to @${task.username}`);

        try {
            // Wait for profile page to load
            await sleep(3000);

            // Find the message/DM button
            const dmButton = safeQuery(document, SELECTORS.dmButton);
            if (!dmButton) {
                dmLog('DM button not found on profile', 'error');
                lsSet('dmTaskResult', {
                    username: task.username,
                    success: false,
                    error: 'DM button not found',
                    logs,
                });
                return;
            }

            dmLog('Found DM button, clicking...');
            dmButton.click();
            await sleep(3000);

            // Wait for chat composer to appear
            let composer = null;
            let attempts = 0;

            while (!composer && attempts < 10) {
                composer = safeQuery(document, SELECTORS.chatComposer);
                if (!composer) {
                    attempts++;
                    await sleep(1000);
                }
            }

            if (!composer) {
                dmLog('Chat composer not found after 10 attempts', 'error');
                lsSet('dmTaskResult', {
                    username: task.username,
                    success: false,
                    error: 'Chat composer not found',
                    logs,
                });
                return;
            }

            dmLog('Chat composer found, inserting message...');

            // Insert text
            composer.focus();
            await sleep(500);

            const inserted = document.execCommand('insertText', false, task.message);
            if (!inserted || !composer.textContent.includes(task.message.substring(0, 20))) {
                // Fallback: clipboard paste
                try {
                    const dataTransfer = new DataTransfer();
                    dataTransfer.setData('text/plain', task.message);
                    composer.dispatchEvent(new ClipboardEvent('paste', {
                        bubbles: true,
                        cancelable: true,
                        clipboardData: dataTransfer,
                    }));
                    await sleep(500);
                } catch (e) {
                    dmLog(`Paste fallback failed: ${e}`, 'warn');
                }

                // Second fallback: direct set
                if (!composer.textContent.includes(task.message.substring(0, 20))) {
                    composer.textContent = task.message;
                    composer.dispatchEvent(new Event('input', { bubbles: true }));
                    await sleep(500);
                }
            }

            if (!composer.textContent.includes(task.message.substring(0, 20))) {
                dmLog('Failed to insert message text', 'error');
                lsSet('dmTaskResult', {
                    username: task.username,
                    success: false,
                    error: 'Text insertion failed',
                    logs,
                });
                return;
            }

            dmLog('Message text inserted, finding send button...');

            // Find and click send
            const sendBtn = safeQuery(document, SELECTORS.sendButton);
            if (!sendBtn) {
                dmLog('Send button not found', 'error');
                lsSet('dmTaskResult', {
                    username: task.username,
                    success: false,
                    error: 'Send button not found',
                    logs,
                });
                return;
            }

            dmLog('Clicking send button...');
            sendBtn.click();
            await sleep(2000);

            dmLog('DM sent successfully', 'action');
            lsSet('dmTaskResult', {
                username: task.username,
                success: true,
                logs,
            });

        } catch (e) {
            dmLog(`DM error: ${e}`, 'error');
            lsSet('dmTaskResult', {
                username: task.username,
                success: false,
                error: String(e),
                logs,
            });
        }
    }

    /*******************************
     *  REPLY AUTOMATION           *
     *******************************/

    /**
     * Post a public reply to a comment.
     */
    async function replyToComment(commentEl, message) {
        devLog(`Posting reply: "${message.substring(0, 40)}..."`, 'info');

        try {
            // Scroll comment into view
            commentEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            await randDelay(CONFIG.perActionDelayMs);

            // Optionally like the comment
            if (CONFIG.likeBeforeReply) {
                const likeBtn = safeQuery(commentEl, SELECTORS.likeButton);
                if (likeBtn) {
                    likeBtn.click();
                    devLog('Liked comment', 'action');
                    await randDelay([1000, 3000]);
                }
            }

            // Click reply button — try selectors first, then text-based fallback
            let replyBtn = safeQuery(commentEl, SELECTORS.replyButton);

            if (!replyBtn) {
                // Fallback: find any element with "Reply" text inside the comment
                const allEls = commentEl.querySelectorAll('span, p, div, a');
                for (const el of allEls) {
                    const text = el.textContent.trim().toLowerCase();
                    if (text === 'reply') {
                        replyBtn = el;
                        devLog('Found reply button via text fallback', 'info');
                        break;
                    }
                }
            }

            if (!replyBtn) {
                // Second fallback: look in parent/sibling containers
                const parent = commentEl.parentElement;
                if (parent) {
                    const allEls = parent.querySelectorAll('span, p, div, a');
                    for (const el of allEls) {
                        const text = el.textContent.trim().toLowerCase();
                        if (text === 'reply') {
                            replyBtn = el;
                            devLog('Found reply button via parent text fallback', 'info');
                            break;
                        }
                    }
                }
            }

            if (!replyBtn) {
                devLog('Reply button not found (tried selectors + text fallback)', 'warn');
                return false;
            }

            replyBtn.click();
            await sleep(1500);

            // Wait for reply input to appear
            let replyInput = null;
            let attempts = 0;

            while (!replyInput && attempts < 10) {
                // The reply input may appear in different places depending on TikTok version
                replyInput = safeQuery(document, SELECTORS.replyInput);
                if (!replyInput) {
                    attempts++;
                    await sleep(1000);
                }
            }

            if (!replyInput) {
                devLog(`Reply textbox not found after ${attempts} attempts`, 'error');
                return false;
            }

            // Type the reply
            const typed = await typeText(replyInput, message);
            if (!typed) {
                devLog('Failed to type reply text', 'error');
                return false;
            }

            await sleep(500);

            // Click submit
            const submitBtn = safeQuery(document, SELECTORS.replySubmit);
            if (!submitBtn) {
                devLog('Reply submit button not found', 'error');
                return false;
            }

            submitBtn.click();
            await sleep(2000);

            devLog(`Reply posted: "${message}"`, 'action');
            return true;

        } catch (e) {
            devLog(`Reply error: ${e}`, 'error');
            return false;
        }
    }

    /*******************************
     *  MAIN PROCESSOR             *
     *******************************/
    async function runProcessor() {
        if (isProcessing) {
            devLog('Already processing', 'warn');
            return;
        }

        isProcessing = true;
        processingController = { abort: false };

        try {
            devLog('=== Processing started ===', 'action');

            // Step 1: Scroll to load comments
            await autoScrollComments();

            if (processingController.abort) {
                devLog('Processing aborted', 'warn');
                return;
            }

            // Step 2: Analyze comments
            const matches = await analyzeComments();

            if (matches.length === 0) {
                devLog('No keyword matches found. Processing complete.', 'action');
                return;
            }

            devLog(`Processing ${matches.length} keyword matches...`, 'action');

            // Step 3: Process each match
            let processedCount = 0;

            for (const match of matches) {
                if (processingController.abort) {
                    devLog('Processing aborted by user', 'warn');
                    break;
                }

                devLog(`\n--- Processing @${match.username} ---`, 'info');

                // Rate limit check
                await waitForRateLimit();
                updateRateLimitDisplay();

                if (processingController.abort) break;

                // Step 3a: Check follower status
                const { isFollower, isMutual } = await checkFollowerStatus(match.username, match.profileUrl);

                await randDelay(CONFIG.perActionDelayMs);

                if (processingController.abort) break;

                if (isFollower || isMutual) {
                    // Step 3b: Follower — attempt DM
                    devLog(`@${match.username} is a follower — attempting DM`, 'action');

                    const dmSuccess = await sendDM(match.username, match.profileUrl, CONFIG.msgFollower);

                    if (dmSuccess && CONFIG.enableMsgAfterDM) {
                        // Post follow-up comment
                        await randDelay(CONFIG.perActionDelayMs);
                        const followUpMsg = pickRandom(CONFIG.msgsAfterDM);
                        await replyToComment(match.element, followUpMsg);
                        await recordReply();
                    } else if (!dmSuccess) {
                        devLog(`DM failed for @${match.username} — posting non-follower reply as fallback`, 'warn');
                        const replyMsg = pickRandom(CONFIG.msgsNonFollower);
                        const replied = await replyToComment(match.element, replyMsg);
                        if (replied) await recordReply();
                    }
                } else {
                    // Step 3c: Non-follower — public reply
                    devLog(`@${match.username} is not a follower — posting public reply`, 'info');
                    const replyMsg = pickRandom(CONFIG.msgsNonFollower);
                    const replied = await replyToComment(match.element, replyMsg);
                    if (replied) await recordReply();
                }

                processedCount++;
                updateRateLimitDisplay();

                if (CONFIG.stopOnError && processedCount === 0) {
                    devLog('Stopping on first error (stopOnError enabled)', 'error');
                    break;
                }
            }

            devLog(`\n=== Processing complete: ${processedCount}/${matches.length} comments processed ===`, 'action');

        } catch (e) {
            devLog(`Processor error: ${e}`, 'error');
        } finally {
            isProcessing = false;
            processingController = null;
        }
    }

    /*******************************
     *  UI CARD                    *
     *******************************/
    let _rateLimitDisplay = null;

    function updateRateLimitDisplay() {
        if (!_rateLimitDisplay) return;
        const s = getRateLimitStatus();
        const nextIn = s.nextInMs > 0 ? `${Math.ceil(s.nextInMs / 1000)}s` : 'now';
        _rateLimitDisplay.textContent = `Replies: ${s.session}/${s.maxSession} session | ${s.hourly}/${s.maxHourly} hour | Next in: ${nextIn}${s.cooldownActive ? ' | COOLDOWN' : ''}`;
    }

    function createUI() {
        // Don't show on non-video pages (but do show on profile pages for DM handling)
        if (!isVideoPage()) return;

        loadSettings();

        const ACCENT = '#fe2c55'; // TikTok red/pink

        // ---- CARD CONTAINER ----
        const card = document.createElement('div');
        card.id = 'tt-cp-card';
        card.style.cssText = `
            position: fixed;
            bottom: 16px;
            left: 16px;
            width: 380px;
            max-height: 90vh;
            background: #0f0f0f;
            border: 2px solid ${ACCENT};
            border-radius: 12px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: #e2e8f0;
            z-index: 999999;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(254, 44, 85, 0.3);
        `;

        // ---- HEADER ----
        const header = document.createElement('div');
        header.style.cssText = `
            background: linear-gradient(135deg, ${ACCENT}, #25f4ee);
            padding: 10px 14px;
            font-weight: 700;
            font-size: 14px;
            color: white;
            cursor: pointer;
            user-select: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
        `;
        header.innerHTML = '<span>TikTok Comment Processor</span><span id="tt-cp-toggle">▼</span>';

        const content = document.createElement('div');
        content.id = 'tt-cp-content';
        content.style.cssText = 'padding: 12px; overflow-y: auto; max-height: 75vh;';

        let collapsed = false;
        header.addEventListener('click', () => {
            collapsed = !collapsed;
            content.style.display = collapsed ? 'none' : 'block';
            document.getElementById('tt-cp-toggle').textContent = collapsed ? '▶' : '▼';
            lsSet('uiState', { collapsed });
        });

        // Restore collapse state
        const uiState = lsGet('uiState');
        if (uiState && uiState.collapsed) {
            collapsed = true;
            content.style.display = 'none';
        }

        // ---- FIELD STYLES ----
        const labelStyle = 'display:block;font-size:11px;color:#94a3b8;margin:8px 0 4px;font-weight:600;';
        const inputStyle = `
            width: 100%;
            box-sizing: border-box;
            background: #1a1a2e;
            border: 1px solid #2d2d44;
            border-radius: 6px;
            color: #e2e8f0;
            padding: 6px 10px;
            font-size: 12px;
            font-family: inherit;
        `;
        const textareaStyle = inputStyle + 'resize:vertical;min-height:50px;';

        // Helper to create labeled field
        function addField(label, type, id, value, placeholder) {
            const lbl = document.createElement('label');
            lbl.style.cssText = labelStyle;
            lbl.textContent = label;
            content.appendChild(lbl);

            let el;
            if (type === 'textarea') {
                el = document.createElement('textarea');
                el.style.cssText = textareaStyle;
                el.value = value || '';
            } else if (type === 'toggle') {
                el = document.createElement('div');
                el.style.cssText = 'display:flex;align-items:center;gap:8px;';
                const toggle = document.createElement('input');
                toggle.type = 'checkbox';
                toggle.checked = !!value;
                toggle.id = id;
                toggle.style.cssText = 'accent-color:' + ACCENT;
                const span = document.createElement('span');
                span.textContent = 'Enabled';
                span.style.cssText = 'font-size:12px;color:#94a3b8;';
                el.appendChild(toggle);
                el.appendChild(span);
                content.appendChild(el);
                return toggle;
            } else {
                el = document.createElement('input');
                el.type = 'text';
                el.style.cssText = inputStyle;
                el.value = value || '';
            }

            if (placeholder) el.placeholder = placeholder;
            el.id = id;
            content.appendChild(el);
            return el;
        }

        // Helper for message group (up to 3 variations)
        function addMessageGroup(label, id, messages) {
            const lbl = document.createElement('label');
            lbl.style.cssText = labelStyle;
            lbl.textContent = label;
            content.appendChild(lbl);

            const container = document.createElement('div');
            container.id = id;
            container.style.cssText = 'display:flex;flex-direction:column;gap:4px;';

            for (let i = 0; i < 3; i++) {
                const ta = document.createElement('textarea');
                ta.style.cssText = textareaStyle + 'min-height:36px;';
                ta.value = messages[i] || '';
                ta.placeholder = i === 0 ? 'Required' : 'Optional variation ' + (i + 1);
                ta.dataset.index = i;
                container.appendChild(ta);
            }

            content.appendChild(container);
            return container;
        }

        // ---- FIELDS ----
        const keywordInput = addField('Search Keyword', 'text', 'tt-cp-keyword', CONFIG.keyword, 'e.g. LINK');
        const dmMsgInput = addField('DM Message for Followers', 'textarea', 'tt-cp-dm-msg', CONFIG.msgFollower, 'Message to DM followers...');
        const nonFollowerGroup = addMessageGroup('Reply Templates for Non-Followers', 'tt-cp-nf-msgs', CONFIG.msgsNonFollower);
        const afterDMGroup = addMessageGroup('Follow-up After DM', 'tt-cp-after-dm-msgs', CONFIG.msgsAfterDM);
        const afterDMToggle = addField('Enable Follow-up After DM', 'toggle', 'tt-cp-after-dm-toggle', CONFIG.enableMsgAfterDM);
        const tagsInput = addField('Author Follow-up Keywords', 'text', 'tt-cp-tags', CONFIG.followUpTags.join(', '), 'Comma-separated skip keywords');
        const likeToggle = addField('Like Before Reply', 'toggle', 'tt-cp-like-toggle', CONFIG.likeBeforeReply);

        // ---- RATE LIMIT DISPLAY ----
        const rateLimitDiv = document.createElement('div');
        rateLimitDiv.style.cssText = `
            margin: 10px 0 6px;
            padding: 6px 10px;
            background: #1a1a2e;
            border: 1px solid #2d2d44;
            border-radius: 6px;
            font-size: 11px;
            color: #94a3b8;
            text-align: center;
        `;
        rateLimitDiv.textContent = 'Replies: 0/100 session | 0/50 hour | Next in: now';
        _rateLimitDisplay = rateLimitDiv;
        content.appendChild(rateLimitDiv);

        // ---- BUTTONS ----
        const btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:6px;margin-top:10px;flex-wrap:wrap;';

        function makeBtn(text, color, onClick) {
            const btn = document.createElement('button');
            btn.textContent = text;
            btn.style.cssText = `
                flex: 1;
                min-width: 70px;
                padding: 8px 0;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
                cursor: pointer;
                color: white;
                background: ${color};
            `;
            btn.addEventListener('click', onClick);
            return btn;
        }

        // Sync UI → CONFIG
        function syncConfig() {
            CONFIG.keyword = keywordInput.value.trim() || CONFIG.keyword;
            CONFIG.msgFollower = dmMsgInput.value.trim() || CONFIG.msgFollower;

            // Non-follower messages
            const nfTextareas = nonFollowerGroup.querySelectorAll('textarea');
            CONFIG.msgsNonFollower = Array.from(nfTextareas)
                .map(ta => ta.value.trim())
                .filter(Boolean);
            if (CONFIG.msgsNonFollower.length === 0) {
                CONFIG.msgsNonFollower = ['Hey! Follow me and shoot me a DM and I\'ll send you the link!'];
            }

            // After DM messages
            const adTextareas = afterDMGroup.querySelectorAll('textarea');
            CONFIG.msgsAfterDM = Array.from(adTextareas)
                .map(ta => ta.value.trim())
                .filter(Boolean);
            if (CONFIG.msgsAfterDM.length === 0) {
                CONFIG.msgsAfterDM = ['Sent!'];
            }

            CONFIG.enableMsgAfterDM = afterDMToggle.checked;

            // Tags
            const tagsVal = tagsInput.value.trim();
            CONFIG.followUpTags = tagsVal ? tagsVal.split(',').map(t => t.trim()).filter(Boolean) : [];

            CONFIG.likeBeforeReply = likeToggle.checked;
        }

        const processBtn = makeBtn('Process', ACCENT, () => {
            syncConfig();
            runProcessor();
        });

        const analyzeBtn = makeBtn('Analyze', '#6366f1', async () => {
            syncConfig();
            devLog('Running analysis only...', 'info');
            await autoScrollComments();
            const matches = await analyzeComments();
            devLog(`\nAnalysis complete: ${matches.length} actionable comments`, 'action');
            for (const m of matches) {
                devLog(`  @${m.username}: "${m.text.substring(0, 60)}..."${m.needsReprocess ? ' [reprocess]' : ''}`, 'info');
            }
        });

        const saveBtn = makeBtn('Save', '#059669', () => {
            syncConfig();
            saveSettings();
        });

        const stopBtn = makeBtn('Stop & Export', '#dc2626', () => {
            if (processingController) {
                processingController.abort = true;
            }
            isProcessing = false;
            devLog('Stop requested — exporting debug snapshot...', 'warn');
            window.__STOP_EXPORT_REQUESTED = true;
        });

        btnRow.appendChild(processBtn);
        btnRow.appendChild(analyzeBtn);
        btnRow.appendChild(saveBtn);
        btnRow.appendChild(stopBtn);
        content.appendChild(btnRow);

        // ---- DEV LOG PANEL ----
        const devLogSection = document.createElement('div');
        devLogSection.style.cssText = 'margin-top: 10px;';
        const devLogLabel = document.createElement('div');
        devLogLabel.style.cssText = labelStyle;
        devLogLabel.textContent = 'Activity Log';
        devLogSection.appendChild(devLogLabel);

        const devLogPanel = document.createElement('div');
        devLogPanel.id = 'tt-cp-devlog';
        devLogPanel.style.cssText = `
            background: #0a0a14;
            padding: 6px 8px;
            border-radius: 6px;
            font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
            font-size: 11px;
            max-height: 180px;
            overflow-y: auto;
            line-height: 1.4;
            border: 1px solid #1e293b;
        `;
        const initLine = document.createElement('div');
        initLine.style.cssText = 'color:#4ade80;padding:2px 0;';
        initLine.textContent = `${new Date().toLocaleTimeString()} >>> TikTok Comment Processor v1.0 ready`;
        devLogPanel.appendChild(initLine);

        // Wire up the global reference
        _devLogPanel = devLogPanel;

        // Replay any entries that were logged before the panel existed
        for (const entry of _devLogEntries) {
            const line = document.createElement('div');
            line.style.cssText = `
                padding: 2px 0;
                border-bottom: 1px solid #1a1a2e;
                font-size: 11px;
                line-height: 1.4;
                word-break: break-word;
                color: ${entry.level === 'action' ? '#4ade80' : entry.level === 'error' ? '#f87171' : entry.level === 'warn' ? '#fbbf24' : '#94a3b8'};
            `;
            line.textContent = `${entry.time} ${entry.text}`;
            devLogPanel.appendChild(line);
        }

        devLogSection.appendChild(devLogPanel);
        content.appendChild(devLogSection);

        card.appendChild(header);
        card.appendChild(content);
        document.body.appendChild(card);

        devLog('UI card rendered', 'info');
        updateRateLimitDisplay();
    }

    /*******************************
     *  PROFILE MODE UI            *
     *******************************/
    function createProfileUI() {
        loadSettings();

        const ACCENT = '#fe2c55';

        const card = document.createElement('div');
        card.id = 'tt-cp-profile-card';
        card.style.cssText = `
            position: fixed;
            bottom: 16px;
            left: 16px;
            width: 380px;
            max-height: 90vh;
            background: #0f0f0f;
            border: 2px solid ${ACCENT};
            border-radius: 12px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: #e2e8f0;
            z-index: 999999;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(254, 44, 85, 0.3);
        `;

        const header = document.createElement('div');
        header.style.cssText = `
            background: linear-gradient(135deg, ${ACCENT}, #25f4ee);
            padding: 10px 14px;
            font-weight: 700;
            font-size: 14px;
            color: white;
        `;
        header.textContent = 'TikTok CP — Profile Mode';

        const content = document.createElement('div');
        content.style.cssText = 'padding: 12px;';

        const labelStyle = 'display:block;font-size:11px;color:#94a3b8;margin:8px 0 4px;font-weight:600;';
        const inputStyle = `
            width: 100%;
            box-sizing: border-box;
            background: #1a1a2e;
            border: 1px solid #2d2d44;
            border-radius: 6px;
            color: #e2e8f0;
            padding: 6px 10px;
            font-size: 12px;
            font-family: inherit;
        `;
        const textareaStyle = inputStyle + 'resize:vertical;min-height:50px;';

        // DM Message field
        const dmLbl = document.createElement('label');
        dmLbl.style.cssText = labelStyle;
        dmLbl.textContent = 'DM Message for Followers';
        content.appendChild(dmLbl);
        const dmInput = document.createElement('textarea');
        dmInput.style.cssText = textareaStyle;
        dmInput.value = CONFIG.msgFollower;
        dmInput.id = 'tt-cp-profile-dm';
        content.appendChild(dmInput);

        // Non-follower reply templates
        const nfLbl = document.createElement('label');
        nfLbl.style.cssText = labelStyle;
        nfLbl.textContent = 'Reply Templates for Non-Followers (up to 3)';
        content.appendChild(nfLbl);
        const nfContainer = document.createElement('div');
        nfContainer.style.cssText = 'display:flex;flex-direction:column;gap:4px;';
        for (let i = 0; i < 3; i++) {
            const ta = document.createElement('textarea');
            ta.style.cssText = textareaStyle + 'min-height:36px;';
            ta.value = CONFIG.msgsNonFollower[i] || '';
            ta.placeholder = i === 0 ? 'Required' : `Optional variation ${i + 1}`;
            nfContainer.appendChild(ta);
        }
        content.appendChild(nfContainer);

        // Info text
        const info = document.createElement('div');
        info.style.cssText = 'font-size:11px;color:#64748b;margin:10px 0;line-height:1.5;';
        info.innerHTML = `
            <strong>Profile mode</strong> will scroll your profile to find all videos,
            then process each one (newest first). The keyword is <strong>auto-detected</strong>
            per video from the most common short comment.<br><br>
            Videos with no clear keyword comment pattern are skipped.
        `;
        content.appendChild(info);

        // Status display
        const statusDiv = document.createElement('div');
        statusDiv.id = 'tt-cp-profile-status';
        statusDiv.style.cssText = `
            margin: 8px 0;
            padding: 8px 10px;
            background: #1a1a2e;
            border: 1px solid #2d2d44;
            border-radius: 6px;
            font-size: 12px;
            color: #94a3b8;
        `;
        statusDiv.textContent = 'Ready — click "Scan & Process All" to start';
        content.appendChild(statusDiv);

        // Buttons
        const btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:6px;margin-top:10px;';

        function makeBtn(text, color, onClick) {
            const btn = document.createElement('button');
            btn.textContent = text;
            btn.style.cssText = `
                flex: 1;
                padding: 10px 0;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                cursor: pointer;
                color: white;
                background: ${color};
            `;
            btn.addEventListener('click', onClick);
            return btn;
        }

        const scanBtn = makeBtn('Scan & Process All', ACCENT, async () => {
            // Sync settings from UI
            CONFIG.msgFollower = dmInput.value.trim() || CONFIG.msgFollower;
            const nfTextareas = nfContainer.querySelectorAll('textarea');
            CONFIG.msgsNonFollower = Array.from(nfTextareas).map(ta => ta.value.trim()).filter(Boolean);
            if (CONFIG.msgsNonFollower.length === 0) {
                CONFIG.msgsNonFollower = ['Hey! Follow me and shoot me a DM and I\'ll send you the link!'];
            }
            saveSettings();

            statusDiv.textContent = 'Scanning profile for videos...';
            statusDiv.style.color = '#fbbf24';

            const videos = await scrapeProfileVideos();

            if (videos.length === 0) {
                statusDiv.textContent = 'No videos found on this profile.';
                statusDiv.style.color = '#f87171';
                return;
            }

            statusDiv.textContent = `Found ${videos.length} videos. Starting processing...`;
            statusDiv.style.color = '#4ade80';

            await startProfileMode(videos);
        });

        const scanOnlyBtn = makeBtn('Scan Only', '#6366f1', async () => {
            statusDiv.textContent = 'Scanning profile for videos...';
            statusDiv.style.color = '#fbbf24';

            const videos = await scrapeProfileVideos();
            statusDiv.textContent = `Found ${videos.length} videos. Click "Scan & Process All" to start.`;
            statusDiv.style.color = '#4ade80';

            // Log first 10
            for (let i = 0; i < Math.min(10, videos.length); i++) {
                devLog(`  ${i + 1}. ${videos[i]}`, 'info');
            }
            if (videos.length > 10) devLog(`  ... and ${videos.length - 10} more`, 'info');
        });

        btnRow.appendChild(scanBtn);
        btnRow.appendChild(scanOnlyBtn);
        content.appendChild(btnRow);

        // Dev log panel
        const devLogSection = document.createElement('div');
        devLogSection.style.cssText = 'margin-top: 10px;';
        const devLogLabel = document.createElement('div');
        devLogLabel.style.cssText = labelStyle;
        devLogLabel.textContent = 'Activity Log';
        devLogSection.appendChild(devLogLabel);

        const devLogPanel = document.createElement('div');
        devLogPanel.id = 'tt-cp-devlog';
        devLogPanel.style.cssText = `
            background: #0a0a14;
            padding: 6px 8px;
            border-radius: 6px;
            font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
            font-size: 11px;
            max-height: 180px;
            overflow-y: auto;
            line-height: 1.4;
            border: 1px solid #1e293b;
        `;
        const initLine = document.createElement('div');
        initLine.style.cssText = 'color:#4ade80;padding:2px 0;';
        initLine.textContent = `${new Date().toLocaleTimeString()} >>> Profile Mode ready`;
        devLogPanel.appendChild(initLine);
        _devLogPanel = devLogPanel;

        for (const entry of _devLogEntries) {
            const line = document.createElement('div');
            line.style.cssText = `
                padding: 2px 0;
                border-bottom: 1px solid #1a1a2e;
                font-size: 11px;
                line-height: 1.4;
                word-break: break-word;
                color: ${entry.level === 'action' ? '#4ade80' : entry.level === 'error' ? '#f87171' : entry.level === 'warn' ? '#fbbf24' : '#94a3b8'};
            `;
            line.textContent = `${entry.time} ${entry.text}`;
            devLogPanel.appendChild(line);
        }

        devLogSection.appendChild(devLogPanel);
        content.appendChild(devLogSection);

        card.appendChild(header);
        card.appendChild(content);
        document.body.appendChild(card);
    }

    /*******************************
     *  INIT                       *
     *******************************/
    function init() {
        devLog(`Page loaded: ${window.location.href}`, 'info');
        devLog(`Pathname: ${window.location.pathname}`, 'info');

        const profileModeActive = lsGet('profileModeActive', false);

        if (isVideoPage()) {
            if (profileModeActive) {
                devLog('Video page detected — profile mode active, auto-processing...', 'info');
                createUI();
                setTimeout(() => continueProfileMode(), 3000);
            } else {
                devLog('Video page detected — showing UI', 'info');
                createUI();
            }
        } else if (isProfilePage()) {
            // Check if there's a pending follow check or DM task first
            const followTask = lsGet('followCheck');
            const dmTask = lsGet('dmTask');

            // Only handle follow/DM tasks if they're recent (< 30 seconds old)
            const now = Date.now();
            const followTaskRecent = followTask && followTask.timestamp && (now - followTask.timestamp) < 30000;
            const dmTaskRecent = dmTask && dmTask.timestamp && (now - dmTask.timestamp) < 30000;

            if (followTaskRecent || dmTaskRecent) {
                devLog('Profile page detected — handling follow/DM task', 'info');
                handleProfilePage();
            } else {
                // Clean up stale tasks from previous runs
                if (followTask) {
                    devLog('Cleaning up stale followCheck from previous run', 'info');
                    lsRemove('followCheck');
                }
                if (dmTask) {
                    devLog('Cleaning up stale dmTask from previous run', 'info');
                    lsRemove('dmTask');
                }
                // Also clean up stale profile mode state
                if (profileModeActive) {
                    devLog('Cleaning up stale profileModeActive from previous run', 'info');
                    lsRemove('profileModeActive');
                    lsRemove('videoQueue');
                    lsRemove('videoQueueIndex');
                    lsRemove('profileModeStats');
                }

                devLog('Profile page detected — showing Profile Mode UI', 'info');
                createProfileUI();
            }
        } else {
            devLog(`Not a video or profile page — userscript idle (path: ${window.location.pathname})`, 'info');
        }
    }

    // Run init
    init();

})();
