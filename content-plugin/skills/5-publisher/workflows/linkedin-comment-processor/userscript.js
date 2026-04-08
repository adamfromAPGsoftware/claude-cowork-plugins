// LinkedIn Comment Processor v2.4
// Scans comments on a LinkedIn post for a keyword and reply / accept / DM with human-like delays.
// Original author: ActualAkshay (actualakshay@gmail.com)
// Tampermonkey header stripped — injected via Playwright addInitScript.
//
// Bug fixes applied (6):
//   1. perActionDelayMs: [3000, 800,       → [3000, 8000],
//   2. safeQuercument                      → safeQuery(document
//   3. acveChatBubble                      → activeChatBubble
//   4. safeQutiveChatBubble                → safeQuery(activeChatBubble
//   5. safry(activeChatBubble              → safeQuery(activeChatBubble
//   6. threadsCountRemaing                 → threadsCountRemaining

(function () {
    'use strict';

    /*******************************
     *  CONFIG - edit these values *
     *******************************/
    const CONFIG = {
        keyword: 'AGENT',
        msgConnected: 'Thanks for your comment — I\'ll DM you the details!',
        msgsNotConnected: ['Thanks! Please connect so I can DM you the details.'],
        msgsAfterDM: ['Sent!'],
        followUpTags: [],
        enableMsgNotConnected: true,
        enableMsgAfterDM: true,
        maxCommentsToProcess: 500,
        perActionDelayMs: [1000, 2500],
        typingDelayMsPerChar: [3, 10],
        stopOnError: false,
        debugSleep: false, //For debug sleep
        debugMode: false, //For debug logging
        debugDmSendButton: false, //For preventing dm send button click
        debugReplyButton: false, //For preventing reply button click
    };

    // Global processing state
    let isProcessing = false;
    let processingController = null;
    let openTabs = []; // Track open tabs for cleanup

    // Function to close all open tabs
    function closeAllOpenTabs() {
        log('Closing all open tabs...');
        openTabs.forEach(tab => {
            try {
                if (tab && !tab.closed) {
                    tab.close();
                    log('Closed tab');
                }
            } catch (e) {
                log('Could not close tab:', e.message);
            }
        });
        openTabs = [];
    }

    /***********************
     *  Utility functions  *
     ***********************/
    const debugSleep = (sec = 30) => {
        if (CONFIG?.debugSleep) {
            const ms = sec * 1000;
            log(`Sleeping for ${sec} seconds...`);
            return new Promise(res => setTimeout(res, ms));
        } else {
            return Promise.resolve();
        }
    };
    const sleep = ms => new Promise(res => setTimeout(res, ms));
    const randBetween = (a, b) => a + Math.random() * (b - a);
    const randDelay = async () => await sleep(randBetween(CONFIG.perActionDelayMs[0], CONFIG.perActionDelayMs[1]));
    const pickRandom = (arr) => arr[Math.floor(Math.random() * arr.length)];


    function deepQuerySelector(selector, root = document) {
        // Check in the root itself
        let found = root.querySelector?.(selector);
        if (found) return found;

        // Check inside all shadow roots (recursively)
        const elements = root.querySelectorAll('*');
        for (const el of elements) {
            if (el.shadowRoot) {
                found = deepQuerySelector(selector, el.shadowRoot);
                if (found) return found;
            }
        }
        return null;
    }

    function deepQuerySelectorAll(selector, root = document) {
        let results = [];

        // Search in the current root
        if (root.querySelectorAll) {
            results.push(...root.querySelectorAll(selector));
        }

        // Search recursively inside all shadow roots
        const elements = root.querySelectorAll?.('*') || [];
        for (const el of elements) {
            if (el.shadowRoot) {
                results.push(...deepQuerySelectorAll(selector, el.shadowRoot));
            }
        }

        return results;
    }
    const commentReply = async (el, text) => {
        el.focus();
        await sleep(200);

        // Clear any existing content (e.g. auto-populated @mention)
        const sel = window.getSelection();
        sel.selectAllChildren(el);
        sel.collapseToEnd();

        // Method 1: execCommand insertText (triggers React state updates)
        const inserted = document.execCommand('insertText', false, text);
        log(`commentReply execCommand: ${inserted ? 'OK' : 'FAILED'}`);

        if (!inserted) {
            // Method 2: Clipboard paste simulation
            log('commentReply trying clipboard paste fallback...');
            el.focus();
            try {
                const clipboardData = new DataTransfer();
                clipboardData.setData('text/plain', text);
                const pasteEvent = new ClipboardEvent('paste', {
                    bubbles: true,
                    cancelable: true,
                    clipboardData: clipboardData
                });
                el.dispatchEvent(pasteEvent);
            } catch (pasteErr) {
                log('Clipboard paste failed, using innerHTML fallback');
                el.innerHTML = `<p>${text}</p>`;
            }
        }

        // Fire input events to ensure React picks up the change
        el.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: text }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        await sleep(300);
    };

    const safeQuery = (parent, selectors) => {
        if (!parent) return null;
        for (const s of selectors) {
            const found = parent.querySelector(s);
            if (found) return found;
        }
        return null;
    };

    // Dev log panel — always visible, always logs (regardless of debugMode)
    let _devLogPanel = null;
    const _devLogEntries = [];

    function _appendToDevLog(level, text) {
        const entry = { time: new Date().toLocaleTimeString(), level, text };
        _devLogEntries.push(entry);
        if (_devLogEntries.length > 200) _devLogEntries.shift();

        if (!_devLogPanel) return;
        const line = document.createElement('div');
        line.style.cssText = `
            padding: 2px 0;
            border-bottom: 1px solid #1a1a2e;
            font-size: 11px;
            line-height: 1.4;
            word-break: break-word;
            color: ${level === 'action' ? '#4ade80' : level === 'error' ? '#f87171' : level === 'warn' ? '#fbbf24' : '#94a3b8'};
        `;
        line.textContent = `${entry.time} ${text}`;
        _devLogPanel.appendChild(line);
        _devLogPanel.scrollTop = _devLogPanel.scrollHeight;
    }

    const log = (...args) => {
        const text = args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ');
        console.log('%c[LinkedInProc]', 'color: #0a66c2; font-weight: bold', ...args);
        _appendToDevLog('info', text);
    };

    // High-visibility action log — shows what the script is ABOUT to do
    const logAction = (text) => {
        console.log('%c[ACTION]', 'color: #4ade80; font-weight: bold', text);
        _appendToDevLog('action', `>>> ${text}`);
    };

    const logWarn = (text) => {
        console.warn('%c[LinkedInProc]', 'color: #fbbf24; font-weight: bold', text);
        _appendToDevLog('warn', text);
    };

    const logError = (text) => {
        console.error('%c[LinkedInProc]', 'color: #f87171; font-weight: bold', text);
        _appendToDevLog('error', text);
    };

    /**************************************
     *  Cross-tab messaging coordination  *
     **************************************/

    // Storage helper functions using localStorage
    const storage = {
        set: (key, value) => {
            try {
                localStorage.setItem(`linkedin_dm_${key}`, JSON.stringify(value));
                log('Storage set:', key, value);
            } catch (e) {
                log('Storage set error:', e);
            }
        },
        get: (key) => {
            try {
                const item = localStorage.getItem(`linkedin_dm_${key}`);
                return item ? JSON.parse(item) : null;
            } catch (e) {
                log('Storage get error:', e);
                return null;
            }
        },
        remove: (key) => {
            try {
                localStorage.removeItem(`linkedin_dm_${key}`);
                log('Storage removed:', key);
            } catch (e) {
                log('Storage remove error:', e);
            }
        }
    };

    // Check if we're on a profile page with a DM task
    async function checkForDMTask() {
        const task = storage.get('dmTask');
        if (!task) return;

        // Check if task is older than 10 seconds - if so, delete it
        const currentTime = Date.now();
        const taskAge = currentTime - task.timestamp;
        const maxAge = 10000; // 10 seconds in milliseconds

        if (taskAge > maxAge) {
            log('DM task is too old (', Math.floor(taskAge / 1000), 's > 10s) - deleting task');
            storage.remove('dmTask');
            return;
        }

        const currentUrl = window.location.href;

        log('Checking for DM task. Current URL:', currentUrl);
        log('Task profile URL:', task.profileUrl);
        log('Task age:', Math.floor(taskAge / 1000), 'seconds');

        // Prevent accidental tab closure while processing
        let isProcessing = true;


        try {
            // Check if we're on the target profile
            if (currentUrl.includes('/in/')) {
                log('On profile page, checking if this is the target profile');

                // Give it a moment to ensure URL is fully loaded
                await sleep(500);

                const normalizedCurrent = window.location.pathname.split('?')[0].replace(/\/$/, '');
                const normalizedTarget = new URL(task.profileUrl).pathname.split('?')[0].replace(/\/$/, '');

                log('Normalized current:', normalizedCurrent);
                log('Normalized target:', normalizedTarget);

                if (normalizedCurrent === normalizedTarget) {
                    log('✓ This is the target profile! Proceeding with DM...');
                    await sleep(1200); // Wait for page to fully load

                    const dmLogs = [];
                    const dmLog = (msg) => { log(msg); dmLogs.push(msg); };
                    const result = await sendDMOnProfile(task.message, task.profileName, dmLog);

                    // Report back to main tab immediately (include logs so main tab can display them)
                    storage.set('dmTaskResult', {
                        success: result.success,
                        timestamp: Date.now(),
                        profileUrl: task.profileUrl,
                        reason: result.reason,
                        logs: dmLogs
                    });

                    // Clear the task
                    storage.remove('dmTask');

                    log('DM task completed:', result.success, result.reason ? `(${result.reason})` : '');
                    log('Closing tab...');                    // Mark as no longer processing
                    isProcessing = false;

                    // Close this tab after a short delay
                    await sleep(500);
                    window.close();
                } else {
                    log('Not the target profile, ignoring');
                    // Not the target profile, remove protection
                    isProcessing = false;
                }
            } else {
                // Not a profile page, remove protection
                isProcessing = false;
            }
        } catch (err) {
            log('checkForDMTask error:', err);
            // Ensure protection is removed on error
            isProcessing = false;
        }
    }

    async function sendDMOnProfile(message, profileName, dmLog = log) {
        try {
            dmLog(`[DM] Starting DM flow for ${profileName}`);

            // Step 1: Wait for profile page to load
            let loadAttempts = 0;
            const maxLoadAttempts = 20;

            while (loadAttempts < maxLoadAttempts) {
                const profilePhoto = safeQuery(document, [
                    '[data-view-name="profile-top-card-member-photo"]',
                    '.pv-top-card-profile-picture__container',
                    '.pv-top-card__photo',
                    'button.pv-top-card-profile-picture__container',
                    'button.pv-top-card__photo',
                    '[aria-label="open profile picture"]'
                ]);
                if (profilePhoto) {
                    dmLog('[DM] Profile page loaded');
                    break;
                }
                dmLog(`[DM] Waiting for profile to load (${loadAttempts + 1}/${maxLoadAttempts})`);
                await sleep(600);
                loadAttempts++;
            }

            if (loadAttempts >= maxLoadAttempts) {
                dmLog('[DM] WARN: Profile may not have loaded fully, proceeding anyway');
            }

            // Step 2: Find and click Message button
            const messageBtn = safeQuery(document, [
                'a[data-view-name="profile-primary-message"]',
                'button[aria-label*="Message"]',
                'button.message-anywhere-button',
                'a.message-anywhere-button',
                'button[data-control-name*="message"]',
                'div.pvs-profile-actions button[aria-label*="Message"]',
                'a[href*="messaging/compose"]',
                'button[data-view-name*="message"]',
                'div[data-view-name="profile-primary-message"] a',
                'div[data-view-name="profile-primary-message"] button'
            ]);

            if (!messageBtn || !messageBtn?.textContent?.toLowerCase().includes('message')) {
                // Always log debug info for message button failures
                const allButtons = document.querySelectorAll('button, a');
                const messageRelated = Array.from(allButtons).filter(btn =>
                    (btn.textContent || btn.innerText || '').toLowerCase().includes('message') ||
                    btn.getAttribute('aria-label')?.toLowerCase().includes('message') ||
                    btn.getAttribute('data-view-name')?.includes('message')
                );
                dmLog(`[DM] FAIL: No message button found. ${messageRelated.length} message-related elements on page:`);
                messageRelated.forEach((btn, i) => {
                    dmLog(`[DM]   ${i + 1}. <${btn.tagName.toLowerCase()}> text="${btn.textContent?.trim()?.substring(0, 40)}" aria="${btn.getAttribute('aria-label')}" data-view="${btn.getAttribute('data-view-name')}"`);
                });
                return { success: false, reason: 'no_message_button' };
            }

            const buttonText = (messageBtn.textContent || messageBtn.innerText || '').trim().toLowerCase();
            dmLog(`[DM] Found message button: "${buttonText}"`);

            if (!messageBtn.offsetParent || messageBtn.style.display === 'none' || messageBtn.style.visibility === 'hidden') {
                dmLog('[DM] FAIL: Message button not visible');
                return { success: false, reason: 'button_not_visible' };
            }

            messageBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
            await sleep(300);
            messageBtn.click();
            dmLog('[DM] Clicked Message button');

            await sleep(600);

            // Step 3: Find the chat bubble for this profile
            let activeChatBubble;
            let chatBubbleName;
            const maxAttempts = 10;

            for (let i = 0; i < maxAttempts; i++) {
                await sleep(600);

                // Try multiple selectors for active chat bubbles
                let activeChatBubbleAll = deepQuerySelectorAll(
                    'div.msg-overlay-conversation-bubble--is-active[datmsg-overlay-conversation-bubble-is-minimized="false"]'
                );

                // Fallback: try without the minimized attribute
                if (activeChatBubbleAll.length === 0) {
                    activeChatBubbleAll = deepQuerySelectorAll(
                        'div.msg-overlay-conversation-bubble--is-active'
                    );
                }

                // Fallback: try any visible msg overlay
                if (activeChatBubbleAll.length === 0) {
                    activeChatBubbleAll = deepQuerySelectorAll(
                        'div.msg-overlay-conversation-bubble'
                    );
                }

                dmLog(`[DM] Chat bubbles found: ${activeChatBubbleAll.length} (attempt ${i + 1}/${maxAttempts})`);

                for (const chatBubble of activeChatBubbleAll) {
                    chatBubbleName = chatBubble.querySelector('h2.msg-overlay-bubble-header__title')?.textContent?.trim();

                    if (chatBubbleName?.toLowerCase() === "new message") {
                        chatBubbleName = safeQuery(chatBubble,
                            ['a.msg-compose__profile-link',
                                '.msg-connections-typeahead__top-fixed-section .artdeco-pill__text']
                        )?.textContent?.trim();
                    }

                    dmLog(`[DM] Chat bubble header: "${chatBubbleName}" (looking for: "${profileName}")`);
                    if (chatBubbleName === profileName) {
                        activeChatBubble = chatBubble;
                        break;
                    }
                }
                if (activeChatBubble) break;
            }

            if (!activeChatBubble) {
                dmLog('[DM] FAIL: Chat bubble not found after 10 attempts');
                return { success: false, reason: 'message_chat_not_opened' };
            }

            if (chatBubbleName !== profileName) {
                dmLog(`[DM] FAIL: Chat name mismatch: "${chatBubbleName}" !== "${profileName}"`);
                return { success: false, reason: 'not_connected' };
            }

            // Step 4: Find composer and send button
            const composer = safeQuery(activeChatBubble, [
                'div.msg-form__contenteditable',
                'div.msg-form__contenteditable[contenteditable="true"]',
                'div[role="textbox"][contenteditable="true"]',
                'div[data-placeholder*="Write a message"]',
                'textarea.msg-form__textarea'
            ]);

            const sendBtn = safeQuery(activeChatBubble, [
                'button.msg-form__send-button',
                'button.msg-form__send-btn',
                'button[type="submit"]',
                'button[aria-label*="Send"]',
            ]);

            if (!composer) {
                dmLog('[DM] FAIL: Composer not found. Active chat HTML classes: ' +
                    Array.from(activeChatBubble.querySelectorAll('[contenteditable], [role="textbox"], textarea'))
                        .map(el => `<${el.tagName.toLowerCase()} class="${el.className}" role="${el.getAttribute('role')}">`)
                        .join(', '));
                return { success: false, reason: 'composer_not_found' };
            }

            if (!sendBtn) {
                dmLog('[DM] FAIL: Send button not found. Buttons in chat: ' +
                    Array.from(activeChatBubble.querySelectorAll('button'))
                        .map(b => `"${b.textContent?.trim()?.substring(0, 20)}" aria="${b.getAttribute('aria-label')}"`)
                        .join(', '));
                return { success: false, reason: 'send_button_not_found' };
            }

            dmLog('[DM] Found composer and send button');

            // Step 5: Insert message using clipboard paste simulation
            composer.click();
            composer.focus();
            await sleep(300);

            dmLog(`[DM] Inserting message (${message.length} chars)...`);

            // Method 1: execCommand insertText (works best with React contenteditables)
            const sel = window.getSelection();
            sel.selectAllChildren(composer);
            sel.collapseToStart();

            const inserted = document.execCommand('insertText', false, message);
            dmLog(`[DM] execCommand insertText: ${inserted ? 'OK' : 'FAILED'}`);

            if (!inserted) {
                // Method 2: Clipboard paste simulation
                dmLog('[DM] Trying clipboard paste fallback...');
                composer.focus();
                try {
                    const clipboardData = new DataTransfer();
                    clipboardData.setData('text/plain', message);
                    const pasteEvent = new ClipboardEvent('paste', {
                        bubbles: true,
                        cancelable: true,
                        clipboardData: clipboardData
                    });
                    composer.dispatchEvent(pasteEvent);
                    dmLog('[DM] Clipboard paste dispatched');
                } catch (clipErr) {
                    dmLog(`[DM] Clipboard paste failed: ${clipErr.message}`);
                    // Method 3: innerHTML as last resort
                    dmLog('[DM] Falling back to innerHTML...');
                    composer.innerHTML = `<p>${message}</p>`;
                }
            }

            // Fire all the events LinkedIn might listen to
            composer.dispatchEvent(new Event('input', { bubbles: true }));
            composer.dispatchEvent(new Event('change', { bubbles: true }));
            composer.dispatchEvent(new InputEvent('input', {
                bubbles: true,
                cancelable: true,
                inputType: 'insertText',
                data: message
            }));

            // Hide placeholder
            const placeholder = composer.parentElement?.querySelector('.msg-form__placeholder');
            if (placeholder) {
                placeholder.style.display = 'none';
                placeholder.setAttribute('aria-hidden', 'true');
            }

            await sleep(500);

            // Check composer has content
            const composerContent = (composer.textContent || composer.innerText || '').trim();
            dmLog(`[DM] Composer content length: ${composerContent.length}, send button disabled: ${sendBtn.disabled}`);

            // Step 6: Click send
            if (!CONFIG?.debugDmSendButton) {
                dmLog('[DM] Clicking send button...');
                sendBtn.removeAttribute('disabled');
                sendBtn.click();
                dmLog('[DM] Send button clicked');
            } else {
                await sleep(3000);
                const closeBtn = safeQuery(activeChatBubble,
                    ['button:has(svg[data-test-icon="close-small"])']
                );
                if (closeBtn) closeBtn.click();
                return { success: true };
            }

            await sleep(800);

            // Step 7: Verify message was sent
            const maxWaitTime = 3;
            for (let i = 0; i < maxWaitTime; i++) {
                const currentContent = (composer?.textContent || composer?.innerText || '')?.trim();
                if (currentContent === '') {
                    dmLog('[DM] SUCCESS: Composer cleared — message sent');
                    const closeBtn = safeQuery(activeChatBubble,
                        ['button:has(svg[data-test-icon="close-small"])']
                    );
                    if (closeBtn) closeBtn.click();
                    return { success: true };
                }

                // Try Enter key as alternative
                composer.focus();
                composer.dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'Enter', code: 'Enter', keyCode: 13, which: 13,
                    bubbles: true, cancelable: true
                }));
                dmLog(`[DM] Tried Enter key as fallback (attempt ${i + 1}/${maxWaitTime})`);
                await sleep(1000);
            }

            dmLog('[DM] WARN: Composer still has content — message may not have sent');
            const closeBtn = safeQuery(activeChatBubble,
                ['button:has(svg[data-test-icon="close-small"])']
            );
            if (closeBtn) closeBtn.click();
            return { success: false, reason: 'composer_still_has_content' };
        } catch (err) {
            dmLog(`[DM] ERROR: ${err.message || err}`);
            return { success: false, reason: 'error' };
        }
    }

    /******************************
     *  UI: floating control card  *
     ******************************/
    function injectUI() {
        if (document.getElementById('li-comment-processor-card')) return;

        const card = document.createElement('div');
        card.id = 'li-comment-processor-card';
        card.style.cssText = `
            position: fixed;
            bottom: 0;
            left: 0;
            width: 480px;
            max-height: calc(100vh - 20px);
            display: flex;
            flex-direction: column;
            background: #fff;
            border: 1px solid #dcdcdc;
            margin-left: 8px;
            border-bottom: none;
            border-radius: 8px 8px 0 0;
            font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.08);
            z-index: 999999;
            overflow: hidden;
            transition: all 0.3s ease;
            display: none;
        `;

        // Header
        const header = document.createElement('div');
        header.style.cssText = `
            height: 47px;
            background: #fff;
            border-bottom: 1px solid #dcdcdc;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            cursor: pointer;
        `;
        const title = document.createElement('div');
        title.style.cssText = `font-weight:600;color:#191919;font-size:14px;display:flex;align-items:center;gap:6px;`;
        title.innerHTML = '<span>Comment Processor</span>';

        const toggleBtn = document.createElement('button');
        toggleBtn.innerHTML = '&#90;'; // down arrow
        toggleBtn.style.cssText = `
            border:none;
            background:none;
            color:#666;
            cursor:pointer;
            transition:transform 0.3s;
            display:flex;
            align-items:center;
            justify-content:center;
            padding:4px;
            font-size:12px;
        `;

        header.appendChild(title);
        header.appendChild(toggleBtn);

        // Content
        const content = document.createElement('div');
        content.style.cssText = `
            padding: 16px;
            overflow-y: auto;
            flex: 1;
            min-height: 0;
        `;

        const field = (label, inputEl, toggleable = false, tooltip = null, horizontal = false) => {
            const wrap = document.createElement('div');
            wrap.style.cssText = 'margin-bottom:10px;';

            if (horizontal) {
                // Horizontal layout: label and input on same row
                const row = document.createElement('div');
                row.style.cssText = 'display:flex;align-items:center;gap:8px;';

                const lab = document.createElement('label');
                lab.textContent = label;
                lab.style.cssText = 'font-size:12px;font-weight:600;color:#555;flex-shrink:0;margin-right:4px;';

                row.appendChild(lab);

                // Add tooltip if provided
                if (tooltip) {
                    const helpIcon = document.createElement('span');
                    helpIcon.textContent = '?';
                    helpIcon.style.cssText = `
                        font-size:11px;
                        font-weight:600;
                        color:#666;
                        background:#f0f0f0;
                        border-radius:50%;
                        width:14px;
                        height:14px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        cursor:pointer;
                        transition:background-color 0.2s;
                        position:relative;
                        flex-shrink:0;
                        margin-right:8px;
                    `;

                    // Create tooltip element
                    const tooltipEl = document.createElement('div');
                    tooltipEl.textContent = tooltip;
                    tooltipEl.style.cssText = `
                        position:fixed;
                        background:#333;
                        color:#fff;
                        padding:8px 12px;
                        border-radius:6px;
                        font-size:11px;
                        white-space:normal;
                        max-width:300px;
                        z-index:1000000;
                        opacity:0;
                        visibility:hidden;
                        transition:opacity 0.2s, visibility 0.2s;
                        pointer-events:none;
                        box-shadow:0 2px 8px rgba(0,0,0,0.15);
                        word-wrap:break-word;
                    `;

                    helpIcon.appendChild(tooltipEl);

                    helpIcon.onmouseover = (e) => {
                        helpIcon.style.background = '#e0e0e0';
                        const rect = helpIcon.getBoundingClientRect();
                        tooltipEl.style.left = rect.left + 'px';
                        tooltipEl.style.top = (rect.top - 8) + 'px';
                        tooltipEl.style.transform = 'translateY(-100%)';
                        tooltipEl.style.opacity = '1';
                        tooltipEl.style.visibility = 'visible';
                    };
                    helpIcon.onmouseout = () => {
                        helpIcon.style.background = '#f0f0f0';
                        tooltipEl.style.opacity = '0';
                        tooltipEl.style.visibility = 'hidden';
                    };

                    row.appendChild(helpIcon);
                }

                // Adjust input width for horizontal layout
                inputEl.style.flex = '1';

                row.appendChild(inputEl);

                wrap.appendChild(row);
            } else {
                // Vertical layout (default)
                const labelRow = document.createElement('div');
                labelRow.style.cssText = 'display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;';

                const labelContainer = document.createElement('div');
                labelContainer.style.cssText = 'display:flex;align-items:center;gap:4px;';

                const lab = document.createElement('label');
                lab.textContent = label;
                lab.style.cssText = 'font-size:12px;font-weight:600;color:#555;';

                labelContainer.appendChild(lab);

                // Add tooltip if provided
                if (tooltip) {
                    const helpIcon = document.createElement('span');
                    helpIcon.textContent = '?';
                    helpIcon.style.cssText = `
                        font-size:11px;
                        font-weight:600;
                        color:#666;
                        background: #f0f0f0;
                        border-radius:50%;
                        width:14px;
                        height:14px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        cursor:pointer;
                        transition:background-color 0.2s;
                        position:relative;
                    `;

                    // Create tooltip element
                    const tooltipEl = document.createElement('div');
                    tooltipEl.textContent = tooltip;
                    tooltipEl.style.cssText = `
                        position:fixed;
                        background:#333;
                        color:#fff;
                        padding:8px 12px;
                        border-radius:6px;
                        font-size:11px;
                        white-space:normal;
                        max-width:300px;
                        z-index:1000000;
                        opacity:0;
                        visibility:hidden;
                        transition:opacity 0.2s, visibility 0.2s;
                        pointer-events:none;
                        box-shadow:0 2px 8px rgba(0,0,0,0.15);
                        word-wrap:break-word;
                    `;

                    helpIcon.appendChild(tooltipEl);

                    helpIcon.onmouseover = (e) => {
                        helpIcon.style.background = '#e0e0e0';
                        const rect = helpIcon.getBoundingClientRect();
                        tooltipEl.style.left = rect.left + 'px';
                        tooltipEl.style.top = (rect.top - 8) + 'px';
                        tooltipEl.style.transform = 'translateY(-100%)';
                        tooltipEl.style.opacity = '1';
                        tooltipEl.style.visibility = 'visible';
                    };
                    helpIcon.onmouseout = () => {
                        helpIcon.style.background = '#f0f0f0';
                        tooltipEl.style.opacity = '0';
                        tooltipEl.style.visibility = 'hidden';
                    };

                    labelContainer.appendChild(helpIcon);
                }

                labelRow.appendChild(labelContainer);

                let statusSpan;
                if (toggleable) {
                    statusSpan = document.createElement('span');
                    statusSpan.className = 'toggle-status';
                    statusSpan.textContent = 'Enabled';
                    statusSpan.style.cssText = `
                font-size:12px;
                font-weight:600;
                color:#0a66c2;
                cursor:pointer;
                user-select:none;
                transition:color 0.2s;
            `;
                    labelRow.appendChild(statusSpan);

                    // Toggle logic (no checkbox, just clickable text)
                    statusSpan.addEventListener('click', () => {
                        const isEnabled = statusSpan.textContent === 'Enabled';
                        if (isEnabled) {
                            statusSpan.textContent = 'Disabled';
                            statusSpan.style.color = '#999';
                            inputEl.disabled = true;
                            inputEl.style.opacity = '0.6';
                        } else {
                            statusSpan.textContent = 'Enabled';
                            statusSpan.style.color = '#0a66c2';
                            inputEl.disabled = false;
                            inputEl.style.opacity = '1';
                        }
                    });
                }

                wrap.appendChild(labelRow);
                wrap.appendChild(inputEl);
            }

            return wrap;
        };

        const inputStyle = `
            width: 100%;
            border: 1px solid #dcdcdc;
            border-radius: 6px;
            padding: 8px 10px;
            font-size: 13px;
            box-sizing: border-box;
            transition: border-color .2s, opacity .2s;
            outline: none;
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            box-shadow: none;
            background: white;
        `;
        const textareaStyle = inputStyle + 'resize:vertical;min-height:60px;';

        const keywordInput = document.createElement('input');
        keywordInput.value = CONFIG.keyword;
        keywordInput.style.cssText = inputStyle;
        keywordInput.placeholder = 'Enter keyword to detect';
        keywordInput.id = 'li-cp-keyword';


        const connectedInput = document.createElement('textarea');
        connectedInput.value = CONFIG.msgConnected;
        connectedInput.style.cssText = textareaStyle;

        // Multi-message group builder (up to 3 variations, random selection at runtime)
        function createMessageGroup(initialMessages, maxCount = 3) {
            const container = document.createElement('div');
            container.style.cssText = 'display:flex;flex-direction:column;gap:6px;transition:opacity .2s;width:100%;';

            const _textareas = [];

            const addBtnRow = document.createElement('div');
            const addBtn = document.createElement('span');
            addBtn.textContent = '+ Add variation';
            addBtn.style.cssText = 'font-size:11px;color:#0a66c2;cursor:pointer;font-weight:600;transition:color 0.2s;';
            addBtn.onmouseover = () => addBtn.style.color = '#004182';
            addBtn.onmouseout = () => addBtn.style.color = '#0a66c2';
            addBtn.onclick = () => _addTextarea('', true);
            addBtnRow.appendChild(addBtn);
            container.appendChild(addBtnRow);

            function _updateAddButton() {
                addBtnRow.style.display = _textareas.length >= maxCount ? 'none' : 'block';
            }

            function _updateBadges() {
                const rows = container.querySelectorAll('.msg-group-row');
                rows.forEach((row, i) => {
                    const badge = row.querySelector('.msg-group-badge');
                    if (badge) badge.textContent = String(i + 1);
                });
            }

            function _addTextarea(value = '', showRemove = true) {
                const row = document.createElement('div');
                row.className = 'msg-group-row';
                row.style.cssText = 'display:flex;align-items:flex-start;gap:4px;';

                const badge = document.createElement('span');
                badge.className = 'msg-group-badge';
                badge.textContent = String(_textareas.length + 1);
                badge.style.cssText = 'font-size:10px;font-weight:700;color:#666;background:#f0f0f0;border-radius:50%;width:18px;height:18px;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:8px;';

                const textarea = document.createElement('textarea');
                textarea.value = value;
                textarea.style.cssText = textareaStyle + 'flex:1;';
                textarea.placeholder = _textareas.length === 0 ? 'Primary message' : 'Variation (leave empty to skip)';

                row.appendChild(badge);
                row.appendChild(textarea);

                if (showRemove && _textareas.length > 0) {
                    const removeBtn = document.createElement('span');
                    removeBtn.textContent = '\u00d7';
                    removeBtn.style.cssText = 'font-size:16px;font-weight:700;color:#999;cursor:pointer;flex-shrink:0;margin-top:6px;padding:0 2px;transition:color 0.2s;';
                    removeBtn.onmouseover = () => removeBtn.style.color = '#dc2626';
                    removeBtn.onmouseout = () => removeBtn.style.color = '#999';
                    removeBtn.onclick = () => {
                        const idx = _textareas.indexOf(textarea);
                        if (idx > 0) {
                            _textareas.splice(idx, 1);
                            row.remove();
                            _updateBadges();
                            _updateAddButton();
                        }
                    };
                    row.appendChild(removeBtn);
                }

                _textareas.push(textarea);
                container.insertBefore(row, addBtnRow);
                _updateAddButton();
            }

            // Initialize with provided messages
            initialMessages.forEach((msg, i) => _addTextarea(msg, i > 0));
            _updateAddButton();

            // Custom disabled property for compatibility with toggle logic
            let _disabled = false;
            Object.defineProperty(container, 'disabled', {
                get: () => _disabled,
                set: (val) => {
                    _disabled = val;
                    _textareas.forEach(ta => ta.disabled = val);
                    addBtn.style.pointerEvents = val ? 'none' : 'auto';
                    addBtn.style.opacity = val ? '0.4' : '1';
                }
            });

            container.getMessages = () => _textareas.map(ta => ta.value.trim()).filter(v => v.length > 0);
            container.setMessages = (msgs) => {
                while (_textareas.length > 0) _textareas.pop();
                [...container.querySelectorAll('.msg-group-row')].forEach(r => r.remove());
                msgs.forEach((msg, i) => _addTextarea(msg, i > 0));
                if (msgs.length === 0) _addTextarea('', false);
                _updateAddButton();
            };

            return container;
        }

        const notConnectedGroup = createMessageGroup(CONFIG.msgsNotConnected);
        const afterDMGroup = createMessageGroup(CONFIG.msgsAfterDM);

        // Tags container
        let followUpTags = [...CONFIG.followUpTags];
        const tagsContainer = document.createElement('div');
        tagsContainer.style.cssText = `
            width:100%;
            border:1px solid #dcdcdc;
            border-radius:6px;
            padding:8px 10px;
            font-size:13px;
            box-sizing:border-box;
            min-height:36px;
            background:#fff;
            display:flex;
            flex-wrap:wrap;
            gap:4px;
            align-items:center;
            transition:border-color .2s, box-shadow .2s;
        `;
        tagsContainer.id = 'li-cp-followup-tags';

        const tagsInput = document.createElement('input');
        tagsInput.style.cssText = `
            border: none;
            outline: none;
            flex: 1;
            min-width: 100px;
            font-size: 13px;
            font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: transparent;
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            box-shadow: none;
        `;
        tagsInput.placeholder = 'Add comment keyword...';

        tagsContainer.appendChild(tagsInput);

        // Tags functions
        function addTag(tag) {
            if (!tag.trim() || followUpTags.includes(tag.trim())) return;
            followUpTags.push(tag.trim());
            renderTags();
        }

        function removeTag(tag) {
            followUpTags = followUpTags.filter(t => t !== tag);
            renderTags();
        }

        function renderTags() {
            // Clear existing badges
            const existingBadges = tagsContainer.querySelectorAll('.tag-badge');
            existingBadges.forEach(badge => badge.remove());

            // Add new badges before the input
            followUpTags.forEach(tag => {
                const badge = document.createElement('span');
                badge.className = 'tag-badge';
                badge.style.cssText = `
                    background:#e3f2fd;
                    color: #1565c0;
                    padding:2px 6px;
                    border-radius:12px;
                    font-size:12px;
                    display:inline-flex;
                    align-items:center;
                    gap:4px;
                    margin-right:4px;
                `;

                const text = document.createElement('span');
                text.textContent = tag;

                const removeBtn = document.createElement('span');
                removeBtn.textContent = '\u00d7';
                removeBtn.style.cssText = `
                    cursor:pointer;
                    font-weight:bold;
                    color:#1565c0;
                    margin-left:2px;
                `;
                removeBtn.onclick = () => removeTag(tag);

                badge.appendChild(text);
                badge.appendChild(removeBtn);

                tagsContainer.insertBefore(badge, tagsInput);
            });
        }

        // Event listener for adding tags
        tagsInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                const tag = tagsInput.value.trim();
                if (tag) {
                    addTag(tag);
                    tagsInput.value = '';
               }
            }
        });

        content.appendChild(field('Search Keyword', keywordInput, false, 'The keyword that the bot will search for in comments. Only comments containing this keyword will be processed.', true));
        content.appendChild(field('DM for Connected Users', connectedInput, false, 'The message sent via Direct Message to 1st-degree connections who commented with the keyword.'));
        content.appendChild(field('Comment for Non-Connections', notConnectedGroup, true, 'Up to 3 reply variations for non-connections. A random message is chosen each time. All variations are auto-detected as author follow-up comments.'));
        content.appendChild(field('Follow-up Comment', afterDMGroup, true, 'Up to 3 follow-up comment variations posted after a successful DM. A random message is chosen each time. All variations are auto-detected as author follow-up comments.'));
        content.appendChild(field('Author Follow-up Comment Keywords', tagsContainer, false, 'These keywords are used to detect author comments in threads. If an author comment contains any of these keywords OR the follow-up comment text (sent after successful DM), that thread is ignored (considered already handled). If neither the keywords nor the follow-up comment text are found in an author comment, the thread will be processed normally. Search is case-insensitive and clubbed together - meaning all comments that are follow-up comments which were sent after successful DM can be effectively ignored.'));

        const btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:8px;margin-top:8px;';
        const startBtn = document.createElement('button');
        startBtn.textContent = 'Process';
        startBtn.style.cssText = `
            flex:1;background:#0a66c2;color:white;border:none;
            border-radius:16px;font-weight:600;height:32px;cursor:pointer;
        `;
        const analyzeBtn = document.createElement('button');
        analyzeBtn.textContent = 'Analyze';
        analyzeBtn.style.cssText = `
            flex:1;background:#f59e0b;color:white;border:none;
            border-radius:16px;font-weight:600;height:32px;cursor:pointer;
        `;
        const saveBtn = document.createElement('button');
        saveBtn.textContent = 'Save';
        saveBtn.style.cssText = `
            flex:1;background:white;color:#666;border:1px solid #ccc;
            border-radius:16px;font-weight:600;height:32px;cursor:pointer;
        `;
        btnRow.appendChild(startBtn);
        btnRow.appendChild(analyzeBtn);
        btnRow.appendChild(saveBtn);
        content.appendChild(btnRow);

        // Status area
        const statusDiv = document.createElement('div');
        statusDiv.id = 'li-cp-status';
        statusDiv.style.cssText = `
            margin-top: 12px;
            padding: 8px 12px;
            background: #fff;
            border: 1px solid #cdcdcd;
            border-radius: 6px;
            font-size: 11px;
            color: #666;
            text-align: center;
            font-weight: 500;
        `;
        statusDiv.textContent = 'Ready...';

        content.appendChild(statusDiv);

        // ---- DEV LOG PANEL ----
        const devLogSection = document.createElement('div');
        devLogSection.style.cssText = 'margin-top: 10px;';

        const devLogHeader = document.createElement('div');
        devLogHeader.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 4px;
        `;

        const devLogTitle = document.createElement('span');
        devLogTitle.textContent = 'Activity Log';
        devLogTitle.style.cssText = 'font-size:11px;font-weight:600;color:#555;';

        const stopExportBtn = document.createElement('button');
        stopExportBtn.textContent = 'Stop & Export';
        stopExportBtn.style.cssText = `
            background: #dc2626;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 2px 10px;
            font-size: 10px;
            font-weight: 600;
            cursor: pointer;
            height: 22px;
        `;
        stopExportBtn.onclick = () => {
            logAction('User requested Stop & Export — signalling Playwright...');
            closeAllOpenTabs();
            isProcessing = false;
            // Signal to Playwright's polling loop (window.close doesn't work on the main tab)
            window.__STOP_EXPORT_REQUESTED = true;
        };

        devLogHeader.appendChild(devLogTitle);
        devLogHeader.appendChild(stopExportBtn);
        devLogSection.appendChild(devLogHeader);

        const devLogPanel = document.createElement('div');
        devLogPanel.id = 'li-cp-devlog';
        devLogPanel.style.cssText = `
            background: #0f172a;
            color: #94a3b8;
            border-radius: 6px;
            padding: 8px;
            font-family: "SF Mono", "Fira Code", "Consolas", monospace;
            font-size: 11px;
            max-height: 180px;
            overflow-y: auto;
            line-height: 1.4;
            border: 1px solid #1e293b;
        `;
        const initLine = document.createElement('div');
        initLine.style.cssText = 'color:#4ade80;padding:2px 0;';
        initLine.textContent = `${new Date().toLocaleTimeString()} >>> Comment Processor v2.4 ready`;
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
        // ---- END DEV LOG PANEL ----

        card.appendChild(header);
        card.appendChild(content);
        document.body.appendChild(card);

        // Collapse functionality
        let collapsed = false;
        header.onclick = () => {
            collapsed = !collapsed;
            content.style.display = collapsed ? 'none' : 'flex';
            content.style.flexDirection = 'column';
            toggleBtn.style.transform = collapsed ? 'rotate(180deg)' : 'rotate(0deg)';
            card.style.height = collapsed ? '47px' : 'auto';
            card.style.borderRadius = collapsed ? '8px 8px 0 0' : '8px 8px 0 0';
            saveCollapsedState(); // Save collapsed state when toggled
        };

        // Add save settings functionality
        const saveSettings = () => {
            const settings = {
                keyword: keywordInput.value.trim(),
                msgConnected: connectedInput.value.trim(),
                msgsNotConnected: notConnectedGroup.getMessages(),
                msgsAfterDM: afterDMGroup.getMessages(),
                followUpTags: [...followUpTags],
                enableMsgNotConnected: !notConnectedGroup.disabled,
                enableMsgAfterDM: !afterDMGroup.disabled
            };
            CONFIG.keyword = keywordInput.value.trim();
            CONFIG.msgConnected = connectedInput.value.trim();
            CONFIG.msgsNotConnected = notConnectedGroup.getMessages();
            CONFIG.msgsAfterDM = afterDMGroup.getMessages();
            CONFIG.followUpTags = [...followUpTags];
            CONFIG.enableMsgNotConnected = !notConnectedGroup.disabled;
            CONFIG.enableMsgAfterDM = !afterDMGroup.disabled;
            storage.set('settings', settings);
            log('Settings saved to localStorage');
            const statusEl = document.getElementById('li-cp-status');
            const oldText = statusEl.textContent;
            if (statusEl) {
                statusEl.textContent = 'Settings saved!';
                setTimeout(() => {
                    if (statusEl.textContent === 'Settings saved!') {
                        statusEl.textContent = oldText;
                    }
                }, 2000);
            }
        };

        // Load saved settings
        const loadSettings = () => {
            const saved = storage.get('settings');
            if (saved) {
                keywordInput.value = saved.keyword;
                connectedInput.value = saved.msgConnected;
                // Handle both legacy (single string) and new (array) formats
                const savedNotConnected = Array.isArray(saved.msgsNotConnected) ? saved.msgsNotConnected
                    : saved.msgNotConnected ? [saved.msgNotConnected] : CONFIG.msgsNotConnected;
                const savedAfterDM = Array.isArray(saved.msgsAfterDM) ? saved.msgsAfterDM
                    : saved.msgAfterDM ? [saved.msgAfterDM] : CONFIG.msgsAfterDM;
                notConnectedGroup.setMessages(savedNotConnected);
                afterDMGroup.setMessages(savedAfterDM);
                CONFIG.keyword = saved.keyword;
                CONFIG.msgConnected = saved.msgConnected;
                CONFIG.msgsNotConnected = savedNotConnected;
                CONFIG.msgsAfterDM = savedAfterDM;
                CONFIG.followUpTags = saved.followUpTags;
                CONFIG.enableMsgNotConnected = saved.enableMsgNotConnected;
                CONFIG.enableMsgAfterDM = saved.enableMsgAfterDM;
                // Load follow-up tags
                if (saved.followUpTags) {
                    followUpTags = [...saved.followUpTags];
                    renderTags();
                }

                // Update toggle states
                const notConnectedToggle = notConnectedGroup.previousElementSibling.querySelector('.toggle-status');
                const afterDMToggle = afterDMGroup.previousElementSibling.querySelector('.toggle-status');

                if (notConnectedToggle) {
                    const isEnabled = saved.enableMsgNotConnected !== false;
                    notConnectedToggle.textContent = isEnabled ? 'Enabled' : 'Disabled';
                    notConnectedToggle.style.color = isEnabled ? '#0a66c2' : '#999';
                    notConnectedGroup.disabled = !isEnabled;
                    notConnectedGroup.style.opacity = isEnabled ? '1' : '0.6';
                }

                if (afterDMToggle) {
                    const isEnabled = saved.enableMsgAfterDM !== false;
                    afterDMToggle.textContent = isEnabled ? 'Enabled' : 'Disabled';
                    afterDMToggle.style.color = isEnabled ? '#0a66c2' : '#999';
                    afterDMGroup.disabled = !isEnabled;
                    afterDMGroup.style.opacity = isEnabled ? '1' : '0.6';
                }

                log('Settings loaded from localStorage');
            }
        };

        // Load settings on UI creation
        loadSettings();

        // Load and apply collapsed state
        const loadCollapsedState = () => {
            const saved = storage.get('uiState');
            if (saved && saved.collapsed) {
                collapsed = true;
                content.style.display = 'none';
                toggleBtn.style.transform = 'rotate(180deg)';
                card.style.height = '47px';
            }
        };

        // Save collapsed state
        const saveCollapsedState = () => {
            storage.set('uiState', { collapsed: collapsed });
        };

        // Load collapsed state on UI creation
        loadCollapsedState();

        startBtn.onclick = () => {
            if (isProcessing) {
                // Stop processing by disabling protection and refreshing the page
                log('Processing stopped by user - disabling protection and refreshing page');
                // Disable processing flag immediately
                closeAllOpenTabs();
                isProcessing = false;
                // Now refresh the page
                window.location.reload();
            } else {
                // Start processing
                CONFIG.keyword = keywordInput.value.trim() || CONFIG.keyword;
                CONFIG.msgConnected = connectedInput.value.trim() || CONFIG.msgConnected;
                const ncMsgs = notConnectedGroup.getMessages();
                CONFIG.msgsNotConnected = ncMsgs.length > 0 ? ncMsgs : CONFIG.msgsNotConnected;
                const dmMsgs = afterDMGroup.getMessages();
                CONFIG.msgsAfterDM = dmMsgs.length > 0 ? dmMsgs : CONFIG.msgsAfterDM;
                CONFIG.followUpTags = [...followUpTags];
                CONFIG.enableMsgNotConnected = !notConnectedGroup.disabled;
                CONFIG.enableMsgAfterDM = !afterDMGroup.disabled;
                saveSettings(); // Save settings when starting
                startBtn.textContent = 'Stop';
                startBtn.style.background = '#dc2626'; // Bright red
                runProcessor().finally(() => {
                    // Reset button when processing completes
                    startBtn.textContent = 'Process';
                    startBtn.style.background = '#0a66c2';
                });
            }
        };

        analyzeBtn.onclick = async () => {
            const statusEl = document.getElementById('li-cp-status');

            if (statusEl) statusEl.innerText = 'Analyzing comments...';
            logAction(`Analyzing comments for keyword: "${CONFIG.keyword}"`);
            saveSettings(); // Save settings when starting


            try {
                // Get all loaded and expanded comments
                logAction('Scrolling to load all comments...');
                const commentAnalysis = await analyzeComments();
                // Display results
                const results = `Analysis\nFound ${commentAnalysis?.threadsCountTotal?.total} threads (${commentAnalysis?.threadsCountTotal?.byAuthor} by author, ${commentAnalysis?.threadsCountTotal?.byOther} by others). ${commentAnalysis?.threadsCountTotal?.withSearchKeyword?.total} contain your keyword (${commentAnalysis?.threadsCountTotal?.withSearchKeyword?.withConnectedPeople} from connections, ${commentAnalysis?.threadsCountTotal?.withSearchKeyword?.withNonConnectedPeople} from non-connections). ${commentAnalysis?.threadsCountRemaining?.byConnectedPeople + commentAnalysis?.threadsCountRemaining?.byNonConnectedPeople} still need processing (${commentAnalysis?.threadsCountRemaining?.byConnectedPeople} connections, ${commentAnalysis?.threadsCountRemaining?.byNonConnectedPeople} non-connections).`;

                logAction(`Analysis complete — ${commentAnalysis?.threadsCountRemaining?.byConnectedPeople + commentAnalysis?.threadsCountRemaining?.byNonConnectedPeople} comments to process (${commentAnalysis?.threadsCountRemaining?.byConnectedPeople} connected, ${commentAnalysis?.threadsCountRemaining?.byNonConnectedPeople} non-connected)`);
                if (statusEl) statusEl.innerText = results;
            } catch (err) {
                logError('Read comments error: ' + (err?.message || err?.toString?.() || JSON.stringify(err)));
                console.error('analyzeComments error:', err);
                if (statusEl) statusEl.innerText = 'Error reading comments';
            }
        };

        saveBtn.onclick = () => {
            saveSettings();
        };
    }

    /********************************
     *  Comment discovery & helpers *
     ********************************/
    function findCommentsContainer() {
        const possible = [
            'div.comments-comments-list',
            'div.feed-shared-update-v2__comments',
            'div.scaffold-finite-scroll__content'
        ];

        // First try main document
        for (const sel of possible) {
            const el = document.querySelector(sel);
            if (el) {
                log('Found comments container in main document:', sel);
                return el;
            }
        }

        // Fallback: check iframes (LinkedIn SPA navigation issue)
        const iframes = document.querySelectorAll('iframe[data-testid="interop-iframe"], iframe[src*="/preload/"]');
        for (const iframe of iframes) {
            try {
                const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
                if (iframeDoc) {
                    log('Checking iframe for comments container');
                    for (const sel of possible) {
                        const el = iframeDoc.querySelector(sel);
                        if (el) {
                            log('Found comments container in iframe:', sel);
                            return el;
                        }
                    }
                }
            } catch (e) {
                log('Could not access iframe content (cross-origin):', e.message);
            }
        }

        log('No comments container found, using main document as fallback');
        return document;
    }


    // Function to discover and prepare all comments for processing
    // This expands replies, loads all comments, and returns comments to reply to
    async function analyzeComments() {
        // Scroll to load comments
        await autoScrollComments();
        await sleep(700);

        // Get all comment elements
        const container = findCommentsContainer() || document;
        const allThreads = Array.from(container.querySelectorAll('article.comments-comment-entity')).filter(comment => {
            // Exclude comments that are inside thread containers (replies)
            return !comment.closest('.comments-thread-item');
        });

        // Expand replies for comments without author badges (max 6 iterations per comment, break if author badge found)
        let iter = 0;
        for (const comment of allThreads) {
            const maxIterations = 6;
            for (let i = 0; i < maxIterations; i++) {

                // Look for replies button
                const repliesButton = [...comment.querySelectorAll('button')]
                    .find(btn => btn.textContent.toLowerCase().includes('previous'));

                if (!repliesButton) {
                    break;
                }
                if (i === 0) {
                    await sleep(randBetween(700, 1100));
                    // Scroll to comment to ensure it's visible before processing
                    comment.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    await sleep(randBetween(500, 900));
                }

                // Check if author badge exists anywhere in this comment thread (including expanded replies)
                let allAuthorBadgesInThread = Array.from(comment.querySelectorAll('.comments-comment-meta__badge'))
                    .filter(badge => badge.textContent?.trim().toLowerCase() === 'author');

                let shouldIgnoreThread = false;
                for (const authorBadge of allAuthorBadgesInThread) {
                    if (authorBadge.textContent?.trim().toLowerCase() === 'author') {
                        const authorCommentEl = authorBadge.closest('article.comments-comment-entity');
                        if (authorCommentEl) {
                            const authorCommentText = authorCommentEl.querySelector('.comments-comment-item__main-content')?.textContent?.trim() || '';

                            // Check if comment matches any configured reply messages (supports multiple templates)
                            const endsWithAfterDM = CONFIG.msgsAfterDM.some(msg => msg && authorCommentText.endsWith(msg));
                            const endsWithNotConnected = CONFIG.msgsNotConnected.some(msg => msg && authorCommentText.endsWith(msg));
                            const containsFollowUpTag = CONFIG.followUpTags?.length > 0 && CONFIG.followUpTags.some(keyword =>
                                authorCommentText.toLowerCase().includes(keyword.toLowerCase())
                            );

                            // If any reply template or tag matches, stop expanding replies for this thread
                            if (endsWithAfterDM || endsWithNotConnected || containsFollowUpTag) {
                                log('Author comment detected - ignoring thread:', {
                                    endsWithAfterDM,
                                    endsWithNotConnected,
                                    containsFollowUpTag,
                                    comment: authorCommentText,
                                });
                                shouldIgnoreThread = true;
                                break;
                            }
                        }
                    }
                }

                if (shouldIgnoreThread) {
                    break;
                }


                log(`Clicking replies button (iteration ${i + 1}/${maxIterations})`);
                repliesButton.click();
                await sleep(700);

                if (i === maxIterations - 1) {
                    log('Reached max iterations for reply expansion on this comment');
                }
            }
            iter++;
            // Add random sleep between 0.5 to 2 seconds after processing each comment
            if (iter === allThreads.length) {
                comment.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        // Return all loaded comments with expanded replies
        const currentKeyword = document.getElementById('li-cp-keyword')?.value?.trim();

        // Analyze comments, counts
        const threadsTotal = allThreads.length;
        const threadsByAuthor = allThreads.filter(commentEl => commentEl.querySelector('.comments-comment-meta__container--parent .comments-comment-meta__badge')?.textContent?.trim().toLowerCase() === 'author')?.length;

        const threadsToProcess = allThreads.filter(commentEl => {
            const outerCommentBadge = commentEl.querySelector('.comments-comment-meta__container--parent .comments-comment-meta__badge')?.textContent?.trim().toLowerCase();
            const isAuthorThread = outerCommentBadge === 'author';
            const doesNotHasSearchKeyword = !extractCommentText(commentEl).toLowerCase()?.includes(currentKeyword.toLowerCase());

            if (isAuthorThread || doesNotHasSearchKeyword) {
                return false;
            }
            return true;
        });
        const threadsWithConnectedPeople = [];
        const threadsWithNonConnectedPeople = [];
        const threadsRemainingToProcess = {
            connected: [],
            nonConnected: []
        }
        threadsToProcess.map(commentEl => {
            const { profileUrl, profileName, connectionDegree } = extractProfileInfo(commentEl);
            if (!profileName && !profileUrl) {
                logWarn('Skipping comment — could not extract profile info');
                return;
            }
            const isConnected = connectionDegree === '1st';

            const allAuthorCommentsInThread = Array.from(commentEl.querySelectorAll('.comments-comment-meta__badge'))
                .filter(badge => badge.textContent?.trim().toLowerCase() === 'author')
                .map(badge => badge.closest('article.comments-comment-entity'))
                .filter(el => el != null)
                .map(el => el.querySelector('.comments-comment-item__main-content')?.textContent?.trim() || '');

            // Check what the author has already replied with in this thread (supports multiple templates)
            const hasAfterDMReply = allAuthorCommentsInThread.some(t => CONFIG.msgsAfterDM.some(msg => msg && t.endsWith(msg)));
            const hasNotConnectedReply = allAuthorCommentsInThread.some(t => CONFIG.msgsNotConnected.some(msg => msg && t.endsWith(msg)));
            const hasFollowUpTag = CONFIG.followUpTags?.length > 0 && allAuthorCommentsInThread.some(t => {
                const lc = t.toLowerCase();
                return CONFIG.followUpTags.some(keyword => lc.includes(keyword.toLowerCase()));
            });

            if (isConnected) {
                threadsWithConnectedPeople.push({ commentEl, profileUrl, profileName, connectionDegree });

                // Skip if we already sent the DM follow-up or a custom tag matches
                if (hasAfterDMReply || hasFollowUpTag) {
                    log(`Skipping ${profileName} (connected) — already handled (DM reply or tag match)`);
                } else if (hasNotConnectedReply) {
                    // They were non-connected before but connected now — process them for DM
                    log(`${profileName} was non-connected, now 1st — will DM this time`);
                    threadsRemainingToProcess.connected.push({ commentEl, profileUrl, profileName, connectionDegree });
                } else {
                    threadsRemainingToProcess.connected.push({ commentEl, profileUrl, profileName, connectionDegree });
                }
            }
            else {
                threadsWithNonConnectedPeople.push({ commentEl, profileUrl, profileName, connectionDegree });

                // Skip if any author reply matches (after-DM, not-connected, or custom tag)
                if (hasAfterDMReply || hasNotConnectedReply || hasFollowUpTag) {
                    log(`Skipping ${profileName} (${connectionDegree}) — already handled`);
                } else {
                    threadsRemainingToProcess.nonConnected.push({ commentEl, profileUrl, profileName, connectionDegree });
                }
            }
        })


        return {
            threadsCountTotal: {
                total: threadsTotal,
                byAuthor: threadsByAuthor,
                byOther: threadsTotal - threadsByAuthor,
                withSearchKeyword: {
                    total: threadsToProcess.length,
                    withConnectedPeople: threadsWithConnectedPeople.length,
                    withNonConnectedPeople: threadsWithNonConnectedPeople.length,
                }
            },
            threadsCountRemaining: {
                byConnectedPeople: threadsRemainingToProcess.connected.length,
                byNonConnectedPeople: threadsRemainingToProcess.nonConnected.length,
            },
            threadsWithConnectedPeople,
            threadsWithNonConnectedPeople,
            threadsRemainingToProcess,
        };

    }

    function extractCommentText(el) {
        // get innertext of first div.comments-thread-entity
        const commentText = el.querySelector('div.comments-thread-entity')?.innerText || '';
        return commentText?.replace(/\s+/g, ' ').trim();
    }




    function extractProfileInfo(commentEl) {
        const profileInfo = safeQuery(commentEl, [
            'a[data-view-name="comment-actor-description"]:not(:has(img))',
            'a[href*="/in/"]:not(:has(img))',
        ]);

        const profileUrl = profileInfo?.href?.split('?')[0];
        const profileInfoText = safeQuery(profileInfo, [
            'p',
            'h3.comments-comment-meta__description',
            '.comments-comment-meta__description',
            'h3',
        ])
        const profileName = profileInfoText?.textContent?.trim()?.split('\u2022')[0]?.trim();
        let connectionDegree = null;
        try {
            connectionDegree = profileInfoText?.textContent?.trim()?.split('\u2022')[1]?.trim();
        } catch (e) {
            log('Could not extract connection degree:', e.message);
        }

        return { profileUrl, profileName, connectionDegree };
    }


    async function autoScrollComments(times = 0) {
        const container = findCommentsContainer();

        // If container is from an iframe, we need to scroll the iframe's window instead
        let scrollTarget = window;
        let isIframe = false;
        let doc = document;

        if (container && container.ownerDocument !== document) {
            // Container is from an iframe
            const iframes = document.querySelectorAll('iframe');
            for (const iframe of iframes) {
                try {
                    if (iframe.contentDocument === container.ownerDocument || iframe.contentWindow?.document === container.ownerDocument) {
                        scrollTarget = iframe.contentWindow;
                        doc = iframe.contentDocument || iframe.contentWindow.document;
                        isIframe = true;
                        log('Found iframe scroll target');
                        break;
                    }
                } catch (e) {
                    // Cross-origin iframe, can't access
                }
            }
        }

        // Check if infinite mode is requested (times = 0 or negative)
        const infiniteMode = times <= 0;
        const maxScrolls = infiniteMode ? 500 : times; // Prevent endless loops in infinite mode
        let scrollCount = 0;

        log(`Starting ${infiniteMode ? 'infinite' : 'fixed'} scroll mode (max: ${maxScrolls})`);

        while (scrollCount < maxScrolls) {
            // Scroll first
            if (container === document || !isIframe) {
                // Fallback to window scrolling when no specific container found or not iframe
                scrollTarget.scrollBy(0, 1200 + Math.random() * 400);
            } else {
                // Scroll the container element within the iframe
                container.scrollBy(0, 1200 + Math.random() * 400);
            }

            await sleep(1000 + Math.random() * 800); // Slightly longer wait for infinite mode

            // In infinite mode, check for "Load more comments" button and click it if exists
            if (infiniteMode) {
                // Look for the load more container using multiple selector strategies
                const loadMoreContainer = safeQuery(doc, [
                    'div.comments-comment-list__load-more-container',
                    'div.comments-comments-list__load-more-container',
                    '.comments-comment-list__load-more-container',
                    '.comments-comments-list__load-more-container'
                ]);

                // Check if it's visible (not hidden) and contains a load more button
                const isVisible = loadMoreContainer &&
                    loadMoreContainer.offsetParent !== null &&
                    loadMoreContainer.style.display !== 'none' &&
                    loadMoreContainer.style.visibility !== 'hidden';

                if (isVisible) {
                    // Look for and click the "Load more comments" button
                    const loadMoreButton = safeQuery(loadMoreContainer, [
                        'button.comments-comments-list__load-more-comments-button--cr',
                        'button[aria-label*="Load more comments"]',
                    ]);

                    if (loadMoreButton && !loadMoreButton.disabled) {
                        log('Found "Load more comments" button, clicking...');
                        loadMoreButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        await sleep(500);
                        loadMoreButton.click();
                        log('Clicked load more button');
                        await sleep(2000 + Math.random() * 1000); // Wait longer for content to load
                    } else {
                        log('Load more container found but button is disabled or hidden, stopping infinite scroll');
                        break;
                    }
                } else if (loadMoreContainer) {
                    log('"Load more comments" container exists but is hidden, stopping infinite scroll');
                    break;
                } else {
                    log('No "Load more comments" container found, stopping infinite scroll');
                    break;
                }
            }

            scrollCount++;
        }

        log(`Scrolling ${infiniteMode ? 'complete' : 'done'} after ${scrollCount} scrolls` + (isIframe ? ' (iframe)' : ''));
    }

    /******************************
     *  Core automation functions *
     ******************************/
    async function replyPublicly(commentEl, message) {
        try {
            logAction(`Posting public reply: "${message}"`);

            // Like the comment first
            const likeBtn = safeQuery(commentEl, [
                'button.social-actions-button.react-button__trigger[aria-pressed="false"]',
                'button.react-button__trigger[aria-label*="React Like"]',
                'button[aria-pressed="false"][aria-label*="Like"]'
            ]);
            if (likeBtn) {
                likeBtn.click();
                logAction('Liked comment');
                await sleep(randBetween(300, 600));
            } else {
                log('Like button not found or already liked');
            }

            // Click reply button
            const replyBtn = safeQuery(commentEl, [
                'button.comments-comment-social-bar__reply-action-button--cr',
                'button[aria-label*="Reply"]',
                'button.reply'
            ]);

            if (!replyBtn) {
                logWarn('Reply button not found');
                return false;
            }

            replyBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
            await sleep(randBetween(300, 500));
            replyBtn.click();
            log('Reply button clicked, waiting for editor...');
            await sleep(randBetween(800, 1200));

            // Wait for reply textbox to appear
            let textarea = null;
            let attempts = 0;

            while (!textarea && attempts < 8) {
                // Search within the comment element and its next siblings (reply box may appear after)
                textarea = safeQuery(commentEl, [
                    '.ql-editor[contenteditable="true"]',
                    'div.ql-editor[contenteditable="true"]',
                    'div[role="textbox"][contenteditable="true"]'
                ]);

                // Also search the parent thread container (reply editor may be a sibling)
                if (!textarea) {
                    const threadContainer = commentEl.closest('.comments-comment-entity, .comments-comment-item, [data-id]');
                    if (threadContainer) {
                        textarea = safeQuery(threadContainer, [
                            '.ql-editor[contenteditable="true"]',
                            'div[role="textbox"][contenteditable="true"]'
                        ]);
                    }
                }

                if (!textarea) {
                    await sleep(400);
                    attempts++;
                    log(`Waiting for reply editor... attempt ${attempts}`);
                }
            }

            if (!textarea) {
                logWarn('Reply textbox not found after 8 attempts');
                return false;
            }

            log('Reply editor found, inserting text...');
            await commentReply(textarea, message);
            await sleep(randBetween(300, 500));

            // Find and click submit button
            // Search broadly — the submit button may be in a sibling container
            let postBtn = safeQuery(commentEl, [
                'button.comments-comment-box__submit-button--cr:not([disabled])',
                'button[data-control-name="comment_submit"]:not([disabled])',
                'button[type="submit"]:not([disabled])'
            ]);

            // Broaden search to thread container if not found
            if (!postBtn) {
                const threadContainer = commentEl.closest('.comments-comment-entity, .comments-comment-item, [data-id]');
                if (threadContainer) {
                    postBtn = safeQuery(threadContainer, [
                        'button.comments-comment-box__submit-button--cr:not([disabled])',
                        'button[type="submit"]:not([disabled])'
                    ]);
                }
            }

            if (postBtn && !postBtn.disabled && !CONFIG.debugReplyButton) {
                postBtn.click();
                logAction('Reply posted');
                await sleep(randBetween(500, 800));
                return true;
            } else if (CONFIG.debugReplyButton) {
                logWarn('Debug mode: reply NOT posted (debugReplyButton=true)');
                return true;
            } else {
                logWarn('Submit button not found or disabled');
                return false;
            }

        } catch (err) {
            logError('replyPublicly error: ' + err.message);
            return false;
        }
    }

    // Function to save DM settings for a profile that will be opened in new tab
    function saveDMSettings(profileUrl, profileName, message) {
        try {
            storage.set('dmTask', {
                profileUrl: profileUrl,
                profileName: profileName,
                message: message,
                timestamp: Date.now()
            });

            log('DM settings saved for profile:', profileUrl);
            return true;
        } catch (err) {
            console.error('saveDMSettings error:', err);
            return false;
        }
    }

    // Function to open profile in new tab (this is the only reliable method given LinkedIn's anti-automation measures)
    async function openInNewTab(url) {
        try {
            log('Opening URL in new tab:', url);

            // This is the only method that reliably works for opening new tabs on LinkedIn
            // despite the user's concerns - all "human-like" element clicking approaches are blocked
            const newTab = window.open(url, '_blank');

            if (newTab) {
                // Track the tab for cleanup
                openTabs.push(newTab);
                return true;
            } else {
                log('window.open blocked by popup blocker - user needs to allow popups for LinkedIn');
                return false;
            }

        } catch (err) {
            console.error('openInNewTab error:', err);
            return false;
      }
    }

    // Function to intelligently wait for DM completion by monitoring localStorage
    async function waitForDMCompletion(profileUrl, timeoutMs = 30000) {
        const startTime = Date.now();

        log('Waiting for DM completion on profile:', profileUrl);

        while (Date.now() - startTime < timeoutMs) {
            const result = storage.get('dmTaskResult');

            if (result && result.profileUrl === profileUrl) {
                // Found result for this profile
                storage.remove('dmTaskResult'); // Clean up the result
                // Replay DM tab logs into the main tab's Activity Log
                if (result.logs && result.logs.length > 0) {
                    for (const entry of result.logs) {
                        _appendToDevLog(result.success ? 'info' : 'warn', entry);
                    }
                }
                const status = result.success ? 'SUCCESS' : `FAILED (${result.reason})`;
                logAction(`DM result: ${status}`);
                return result.success;
            }

            // Wait a bit before checking again
            await sleep(500);
        }

        log('DM completion timeout reached for profile:', profileUrl);
        return false; // Timeout reached, assume failure
    }

    /*******************************
     *  Main processing loop       *
     *******************************/
    async function runProcessor() {
        // Create AbortController for cancellation
        processingController = new AbortController();
        const signal = processingController.signal;

        try {
            isProcessing = true;
            const statusEl = document.getElementById('li-cp-status');
            statusEl.innerText = 'Running...';
            logAction(`Starting processor — keyword: "${CONFIG.keyword}"`);

            // Get all loaded and expanded comments
            const analysis = await analyzeComments();
            const { threadsRemainingToProcess } = analysis;

            // Log full analysis so user can see what was found
            const totalMatched = analysis.threadsCountTotal.withSearchKeyword.total;
            const totalRemaining = threadsRemainingToProcess.connected.length + threadsRemainingToProcess.nonConnected.length;
            const skippedCount = totalMatched - totalRemaining;
            logAction(`Found ${analysis.threadsCountTotal.total} threads total (${analysis.threadsCountTotal.byAuthor} by author, ${analysis.threadsCountTotal.byOther} by others)`);
            logAction(`Keyword "${CONFIG.keyword}" matched: ${totalMatched} threads (${analysis.threadsCountTotal.withSearchKeyword.withConnectedPeople} connected, ${analysis.threadsCountTotal.withSearchKeyword.withNonConnectedPeople} non-connected)`);
            if (skippedCount > 0) {
                logAction(`Skipped ${skippedCount} already-handled threads (author reply detected)`);
            }
            logAction(`Still need processing: ${threadsRemainingToProcess.connected.length} connected + ${threadsRemainingToProcess.nonConnected.length} non-connected`);

            if (threadsRemainingToProcess.connected.length === 0 && threadsRemainingToProcess.nonConnected.length === 0) {
                logWarn('No comments remaining to process — either keyword didn\'t match or all threads already handled');
                statusEl.innerText = 'No comments to process. Check keyword or expand "Activity Log" for details.';
                return;
            }

            // Check if cancelled
            if (signal.aborted) {
                log('Processing cancelled');
                return;
            }

            let processed = 0;
            //! Process connected comments

            const totalComments = threadsRemainingToProcess.connected.length + threadsRemainingToProcess.nonConnected.length;
            for (const commentData of threadsRemainingToProcess.connected) {
                processed++;
                const { commentEl, profileUrl, profileName } = commentData;
                statusEl.innerText = `[${processed}/${totalComments}] Processing ${profileName}'s comment`;
                logAction(`[${processed}/${totalComments}] Connected user: ${profileName} — will open profile & send DM`);
                // Step 1: scroll to the comment
                commentEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                await sleep(randBetween(300, 600));
                await randDelay();
                // Check if cancelled
                if (signal.aborted) {
                    logWarn('Processing cancelled by user');
                    return;
                }

                if (!profileUrl || !profileName) {
                    logWarn(`Skipping — no profile URL or name found`);
                    continue;
                }

                // Step 2: save DM settings for the new tab
                logAction(`Opening ${profileName}'s profile in new tab to DM...`);
                saveDMSettings(profileUrl, profileName, CONFIG.msgConnected);
                // Step 3: open profile in new tab with middle-click (less detectable)
                const tabOpened = await openInNewTab(profileUrl);

                if (tabOpened) {
                    log('Profile tab opened successfully, intelligently waiting for DM completion...');
                    const dmSuccess = await waitForDMCompletion(profileUrl);
                    if (dmSuccess) {
                        log('DM completed successfully');
                        // Assume DM was attempted, post success reply if enabled (random selection from templates)
                        if (CONFIG.enableMsgAfterDM) {
                            const chosenMsg = pickRandom(CONFIG.msgsAfterDM);
                            logAction(`Random follow-up selected: "${chosenMsg}"`);
                            await replyPublicly(commentEl, chosenMsg);
                        }
                    } else {
                        log('DM completion failed');
                    }
                } else {
                    log('Failed to open profile tab');
                }
            }

            processed = 0;
            //! Process nonConnected comments
            for (const commentData of threadsRemainingToProcess.nonConnected) {
                processed++;
                const { commentEl, profileUrl, profileName, connectionDegree } = commentData;
                statusEl.innerText = `[${processed}/${totalComments}] Processing ${profileName}'s comment`;
                logAction(`[${processed}/${totalComments}] Non-connected (${connectionDegree}): ${profileName} — will post public reply`);
                // Step 1: scroll to the comment
                commentEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                await sleep(randBetween(300, 600));
                await randDelay();
                // Check if cancelled
                if (signal.aborted) {
                    logWarn('Processing cancelled by user');
                    return;
                }
                if (['2nd', '3rd', '3rd+'].includes(connectionDegree)) {
                    const chosenMsg = pickRandom(CONFIG.msgsNotConnected);
                    logAction(`Random non-connection reply selected: "${chosenMsg}"`);
                    await replyPublicly(commentEl, chosenMsg);
                } else {
                    logWarn(`Skipping ${profileName} — unknown degree: ${connectionDegree}`);
                }
            }

            if (statusEl) statusEl.innerText = `Finished.`;
            log('Processing complete');
        } catch (err) {
            if (err.name === 'AbortError') {
                log('Processing was cancelled');
            } else {
                logError('Processor error: ' + (err?.message || err?.toString?.() || JSON.stringify(err)));
                logError('Stack: ' + (err?.stack || 'no stack'));
                const statusEl = document.getElementById('li-cp-status');
                if (statusEl) statusEl.innerText = 'Error - check Activity Log';
            }
        } finally {
            isProcessing = false;
            processingController = null;

        }
    }

    /*********************
     *  Initialize       *
     *********************/

    log('======================================');
    log('LinkedIn Comment Processor v2.4 loaded');
    log('Current URL:', window.location.href);

    // Check if this is a profile page with a DM task
    if (window.location.href.includes('/in/')) {
        log('Profile page detected, checking for DM task...');
        setTimeout(() => {
            checkForDMTask();
        }, 1000);
    }

    // Always inject UI at startup (hidden by default)
    injectUI();

    // Function to update UI visibility based on current page
    function updateUIVisibility() {
        const currentUrl = window.location.href;
        const uiCard = document.getElementById('li-comment-processor-card');

        if (uiCard) {
            // Check if we're on a post page - show UI
            if (currentUrl.includes('/feed/update') || currentUrl.includes('/posts/')) {
                if (uiCard.style.display === 'none') {
                    log('Navigation detected - showing UI on post page');
                    uiCard.style.display = 'flex';
                }
            } else {
                // Not on a post page - hide UI
                if (uiCard.style.display !== 'none') {
                    log('Navigation detected - hiding UI (not on post page)');
                    uiCard.style.display = 'none';
                }
            }
        }
    }

    // Function to inject UI into iframes when needed
    function injectUIIntoIframe(iframe) {
        try {
            const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
            if (iframeDoc && !iframeDoc.getElementById('li-comment-processor-card')) {
                log('Injecting UI into iframe');

                // Create the UI card in the iframe
                const card = iframeDoc.createElement('div');
                card.id = 'li-comment-processor-card';
                card.style.cssText = `
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    width: 360px;
                    max-height: 600px;
                    background: #fff;
                    border: 1px solid #dcdcdc;
                    margin-left: 8px;
                    border-bottom: none;
                    border-radius: 8px 8px 0 0;
                    font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    box-shadow: 0 -2px 10px rgba(0,0,0,0.08);
                    z-index: 999999;
                    overflow: hidden;
                    transition: all 0.3s ease;
                    display: block;
                `;

                // Simple status display for iframe
                const statusDiv = iframeDoc.createElement('div');
                statusDiv.id = 'li-cp-status';
                statusDiv.style.cssText = `
                    padding: 16px;
                    background: #f0f8ff;
                    border: 1px solid #b3d9ff;
                    border-radius: 6px;
                    font-size: 12px;
                    color: #1e40af;
                    text-align: center;
                    font-weight: 500;
                `;
                statusDiv.textContent = 'Bot active in iframe';

                card.appendChild(statusDiv);
                iframeDoc.body.appendChild(card);

                log('UI injected into iframe successfully');
            }
        } catch (e) {
            log('Could not inject UI into iframe:', e.message);
        }
    }

    // Check for iframes and inject UI when they load
    function checkIframes() {
        const iframes = document.querySelectorAll('iframe[data-testid="interop-iframe"], iframe[src*="/preload/"]');
        iframes.forEach(iframe => {
            if (iframe.contentDocument || iframe.contentWindow) {
                injectUIIntoIframe(iframe);
            }
        });
    }

    // Initial iframe check
    setTimeout(checkIframes, 2000);

    // Periodic check for navigation changes and iframes (every 2 seconds)
    setInterval(() => {
        updateUIVisibility();
        checkIframes();
    }, 2000);

    log('======================================');

})();
