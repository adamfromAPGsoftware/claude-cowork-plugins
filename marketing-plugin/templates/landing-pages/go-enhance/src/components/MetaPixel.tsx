import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";

declare global {
  interface Window {
    fbq: (...args: unknown[]) => void;
  }
}

export default function MetaPixel() {
  const location = useLocation();
  const isFirstRender = useRef(true);

  useEffect(() => {
    // Skip first mount — the base pixel code in index.html already fires PageView
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    if (window.fbq) {
      window.fbq("track", "PageView");
    }
  }, [location]);

  return null;
}
