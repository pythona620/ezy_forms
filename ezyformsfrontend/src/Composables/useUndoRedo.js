/**
 * useUndoRedo Composable
 *
 * Provides undo/redo functionality with history management
 * and keyboard shortcuts support.
 */

import { ref, computed, watch, onMounted, onUnmounted } from 'vue';

export function useUndoRedo(initialState, options = {}) {
  const {
    maxHistorySize = 50,
    debounceMs = 300,
    enableKeyboardShortcuts = true
  } = options;

  // ============================================
  // STATE
  // ============================================

  const history = ref([JSON.parse(JSON.stringify(initialState))]);
  const currentIndex = ref(0);
  const isUndoing = ref(false);
  const isRedoing = ref(false);
  let debounceTimer = null;

  // ============================================
  // COMPUTED
  // ============================================

  const canUndo = computed(() => currentIndex.value > 0);
  const canRedo = computed(() => currentIndex.value < history.value.length - 1);

  const currentState = computed(() => history.value[currentIndex.value]);

  const undoCount = computed(() => currentIndex.value);
  const redoCount = computed(() => history.value.length - currentIndex.value - 1);

  // ============================================
  // METHODS
  // ============================================

  /**
   * Push a new state to history
   */
  function pushState(newState, immediate = false) {
    // Clear debounce timer if immediate
    if (immediate && debounceTimer) {
      clearTimeout(debounceTimer);
      debounceTimer = null;
    }

    const pushFn = () => {
      // Don't push if we're undoing/redoing
      if (isUndoing.value || isRedoing.value) {
        return;
      }

      // Create a deep copy of the state
      const stateCopy = JSON.parse(JSON.stringify(newState));

      // If we're not at the end of history, remove everything after current index
      if (currentIndex.value < history.value.length - 1) {
        history.value = history.value.slice(0, currentIndex.value + 1);
      }

      // Add new state
      history.value.push(stateCopy);

      // Limit history size
      if (history.value.length > maxHistorySize) {
        history.value.shift();
      } else {
        currentIndex.value++;
      }
    };

    if (immediate) {
      pushFn();
    } else {
      // Debounce state pushes
      if (debounceTimer) {
        clearTimeout(debounceTimer);
      }

      debounceTimer = setTimeout(() => {
        pushFn();
        debounceTimer = null;
      }, debounceMs);
    }
  }

  /**
   * Undo to previous state
   */
  function undo() {
    if (!canUndo.value) {
      return null;
    }

    isUndoing.value = true;
    currentIndex.value--;

    // Return the previous state
    const previousState = JSON.parse(JSON.stringify(currentState.value));

    // Reset flag after a short delay to allow watchers to settle
    setTimeout(() => {
      isUndoing.value = false;
    }, 100);

    return previousState;
  }

  /**
   * Redo to next state
   */
  function redo() {
    if (!canRedo.value) {
      return null;
    }

    isRedoing.value = true;
    currentIndex.value++;

    // Return the next state
    const nextState = JSON.parse(JSON.stringify(currentState.value));

    // Reset flag after a short delay
    setTimeout(() => {
      isRedoing.value = false;
    }, 100);

    return nextState;
  }

  /**
   * Jump to a specific point in history
   */
  function jumpTo(index) {
    if (index < 0 || index >= history.value.length) {
      return null;
    }

    const wasUndoing = index < currentIndex.value;
    const wasRedoing = index > currentIndex.value;

    if (wasUndoing) {
      isUndoing.value = true;
    } else if (wasRedoing) {
      isRedoing.value = true;
    }

    currentIndex.value = index;

    const targetState = JSON.parse(JSON.stringify(currentState.value));

    setTimeout(() => {
      isUndoing.value = false;
      isRedoing.value = false;
    }, 100);

    return targetState;
  }

  /**
   * Clear all history
   */
  function clearHistory() {
    history.value = [JSON.parse(JSON.stringify(currentState.value))];
    currentIndex.value = 0;
  }

  /**
   * Reset to initial state
   */
  function reset() {
    history.value = [JSON.parse(JSON.stringify(initialState))];
    currentIndex.value = 0;
  }

  /**
   * Get history snapshot (for debugging)
   */
  function getHistorySnapshot() {
    return {
      history: history.value,
      currentIndex: currentIndex.value,
      canUndo: canUndo.value,
      canRedo: canRedo.value,
      undoCount: undoCount.value,
      redoCount: redoCount.value
    };
  }

  // ============================================
  // KEYBOARD SHORTCUTS
  // ============================================

  function handleKeyDown(event) {
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const modKey = isMac ? event.metaKey : event.ctrlKey;

    // Ctrl/Cmd + Z: Undo
    if (modKey && event.key === 'z' && !event.shiftKey) {
      event.preventDefault();
      if (canUndo.value) {
        const previousState = undo();
        if (previousState) {
          // Emit event or callback can be added here
          console.log('Undo triggered');
        }
      }
    }

    // Ctrl/Cmd + Shift + Z or Ctrl/Cmd + Y: Redo
    if ((modKey && event.key === 'z' && event.shiftKey) || (modKey && event.key === 'y')) {
      event.preventDefault();
      if (canRedo.value) {
        const nextState = redo();
        if (nextState) {
          console.log('Redo triggered');
        }
      }
    }
  }

  // ============================================
  // LIFECYCLE
  // ============================================

  onMounted(() => {
    if (enableKeyboardShortcuts) {
      document.addEventListener('keydown', handleKeyDown);
    }
  });

  onUnmounted(() => {
    if (enableKeyboardShortcuts) {
      document.removeEventListener('keydown', handleKeyDown);
    }

    // Clear debounce timer on unmount
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
  });

  // ============================================
  // RETURN API
  // ============================================

  return {
    // State
    history,
    currentIndex,
    currentState,
    isUndoing,
    isRedoing,

    // Computed
    canUndo,
    canRedo,
    undoCount,
    redoCount,

    // Methods
    pushState,
    undo,
    redo,
    jumpTo,
    clearHistory,
    reset,
    getHistorySnapshot
  };
}
