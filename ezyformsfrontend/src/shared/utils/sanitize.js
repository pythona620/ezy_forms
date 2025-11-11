/**
 * HTML Sanitization Utility
 *
 * Provides safe HTML sanitization to prevent XSS attacks
 * when rendering user-controlled content with v-html
 */

import DOMPurify from 'dompurify';

/**
 * Sanitize HTML string to prevent XSS attacks
 *
 * @param {string} dirty - Unsafe HTML string
 * @param {Object} config - DOMPurify configuration options
 * @returns {string} - Safe HTML string
 */
export function sanitizeHtml(dirty, config = {}) {
  if (!dirty || typeof dirty !== 'string') {
    return '';
  }

  // Default safe configuration
  const defaultConfig = {
    ALLOWED_TAGS: [
      'b', 'i', 'em', 'strong', 'u', 's', 'strike',
      'p', 'br', 'span', 'div',
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'ul', 'ol', 'li',
      'a', 'img',
      'table', 'thead', 'tbody', 'tr', 'th', 'td',
      'blockquote', 'code', 'pre'
    ],
    ALLOWED_ATTR: [
      'href', 'target', 'rel', 'src', 'alt', 'title',
      'class', 'id', 'style'
    ],
    ALLOW_DATA_ATTR: false,
    // Prevent protocol-based XSS (e.g., javascript:, data:)
    ALLOWED_URI_REGEXP: /^(?:(?:https?|mailto|tel|ftp):)/i,
    ...config
  };

  return DOMPurify.sanitize(dirty, defaultConfig);
}

/**
 * Sanitize HTML with strict configuration (minimal tags allowed)
 * Use this for user-generated content that shouldn't have complex formatting
 *
 * @param {string} dirty - Unsafe HTML string
 * @returns {string} - Safe HTML string with minimal tags
 */
export function sanitizeHtmlStrict(dirty) {
  return sanitizeHtml(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'br', 'p'],
    ALLOWED_ATTR: []
  });
}

/**
 * Strip all HTML tags and return plain text
 *
 * @param {string} html - HTML string
 * @returns {string} - Plain text without HTML
 */
export function stripHtml(html) {
  if (!html || typeof html !== 'string') {
    return '';
  }

  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [],
    ALLOWED_ATTR: []
  });
}

/**
 * Vue composable for sanitizing HTML in reactive contexts
 *
 * @example
 * import { useSanitize } from '@/shared/utils/sanitize';
 *
 * const { sanitize } = useSanitize();
 * const safeHtml = computed(() => sanitize(unsafeHtml.value));
 */
export function useSanitize() {
  return {
    sanitize: sanitizeHtml,
    sanitizeStrict: sanitizeHtmlStrict,
    stripHtml
  };
}

export default {
  sanitizeHtml,
  sanitizeHtmlStrict,
  stripHtml,
  useSanitize
};
