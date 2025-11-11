/**
 * useAutoSave Composable
 *
 * Provides automatic saving functionality with debounce,
 * visual feedback, and error handling.
 */

import { ref, computed, watch, onUnmounted } from 'vue';

export function useAutoSave(saveFunction, options = {}) {
  const {
    debounceMs = 2000,
    enabled = true,
    onSaveStart = () => {},
    onSaveSuccess = () => {},
    onSaveError = () => {}
  } = options;

  // ============================================
  // STATE
  // ============================================

  const isSaving = ref(false);
  const lastSaved = ref(null);
  const lastSaveAttempt = ref(null);
  const saveError = ref(null);
  const saveCount = ref(0);
  const isEnabled = ref(enabled);

  let debounceTimer = null;
  let retryTimer = null;
  let dataToSave = null;

  // ============================================
  // COMPUTED
  // ============================================

  const saveStatus = computed(() => {
    if (isSaving.value) {
      return 'saving';
    }

    if (saveError.value) {
      return 'error';
    }

    if (lastSaved.value) {
      return 'saved';
    }

    return 'idle';
  });

  const saveStatusText = computed(() => {
    switch (saveStatus.value) {
      case 'saving':
        return 'Saving...';
      case 'saved':
        return `Saved ${getTimeSinceLastSave()}`;
      case 'error':
        return 'Save failed';
      case 'idle':
      default:
        return 'Not saved';
    }
  });

  const saveStatusIcon = computed(() => {
    switch (saveStatus.value) {
      case 'saving':
        return 'bi bi-arrow-clockwise spin';
      case 'saved':
        return 'bi bi-check-circle-fill';
      case 'error':
        return 'bi bi-exclamation-triangle-fill';
      case 'idle':
      default:
        return 'bi bi-cloud';
    }
  });

  const hasPendingSave = computed(() => {
    return debounceTimer !== null;
  });

  // ============================================
  // METHODS
  // ============================================

  /**
   * Trigger auto-save with debounce
   */
  function triggerSave(data, immediate = false) {
    if (!isEnabled.value) {
      return;
    }

    // Store the data to save
    dataToSave = data;

    // Clear existing timer
    if (debounceTimer) {
      clearTimeout(debounceTimer);
      debounceTimer = null;
    }

    // Clear retry timer if exists
    if (retryTimer) {
      clearTimeout(retryTimer);
      retryTimer = null;
    }

    if (immediate) {
      performSave();
    } else {
      // Set new debounce timer
      debounceTimer = setTimeout(() => {
        performSave();
        debounceTimer = null;
      }, debounceMs);
    }
  }

  /**
   * Perform the actual save operation
   */
  async function performSave() {
    if (!dataToSave || isSaving.value) {
      return;
    }

    try {
      isSaving.value = true;
      lastSaveAttempt.value = new Date();
      saveError.value = null;

      // Call the onSaveStart callback
      onSaveStart();

      // Call the save function
      await saveFunction(dataToSave);

      // Update success state
      lastSaved.value = new Date();
      saveCount.value++;
      saveError.value = null;

      // Call the onSaveSuccess callback
      onSaveSuccess({
        savedAt: lastSaved.value,
        saveCount: saveCount.value
      });
    } catch (error) {
      console.error('Auto-save error:', error);
      saveError.value = error;

      // Call the onSaveError callback
      onSaveError(error);

      // Optionally retry after a delay
      scheduleRetry();
    } finally {
      isSaving.value = false;
    }
  }

  /**
   * Force immediate save (bypass debounce)
   */
  function forceSave(data) {
    dataToSave = data;
    return performSave();
  }

  /**
   * Schedule a retry after failed save
   */
  function scheduleRetry(delayMs = 5000) {
    if (retryTimer) {
      clearTimeout(retryTimer);
    }

    retryTimer = setTimeout(() => {
      if (dataToSave) {
        performSave();
      }
      retryTimer = null;
    }, delayMs);
  }

  /**
   * Cancel pending save
   */
  function cancelSave() {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
      debounceTimer = null;
    }

    if (retryTimer) {
      clearTimeout(retryTimer);
      retryTimer = null;
    }

    dataToSave = null;
  }

  /**
   * Enable auto-save
   */
  function enable() {
    isEnabled.value = true;
  }

  /**
   * Disable auto-save
   */
  function disable() {
    isEnabled.value = false;
    cancelSave();
  }

  /**
   * Get time since last save (human readable)
   */
  function getTimeSinceLastSave() {
    if (!lastSaved.value) {
      return '';
    }

    const seconds = Math.floor((new Date() - lastSaved.value) / 1000);

    if (seconds < 10) {
      return 'just now';
    }

    if (seconds < 60) {
      return `${seconds} seconds ago`;
    }

    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) {
      return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    }

    const hours = Math.floor(minutes / 60);
    return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  }

  /**
   * Reset save state
   */
  function reset() {
    cancelSave();
    isSaving.value = false;
    lastSaved.value = null;
    lastSaveAttempt.value = null;
    saveError.value = null;
    saveCount.value = 0;
    dataToSave = null;
  }

  // ============================================
  // LIFECYCLE
  // ============================================

  onUnmounted(() => {
    // Clean up timers
    cancelSave();
  });

  // ============================================
  // AUTO-UPDATE STATUS TEXT
  // ============================================

  // Update status text every 30 seconds to keep "time ago" current
  let statusUpdateInterval = setInterval(() => {
    // This will trigger the computed to re-evaluate
    if (lastSaved.value) {
      lastSaved.value = new Date(lastSaved.value);
    }
  }, 30000);

  onUnmounted(() => {
    if (statusUpdateInterval) {
      clearInterval(statusUpdateInterval);
    }
  });

  // ============================================
  // RETURN API
  // ============================================

  return {
    // State
    isSaving,
    lastSaved,
    lastSaveAttempt,
    saveError,
    saveCount,
    isEnabled,

    // Computed
    saveStatus,
    saveStatusText,
    saveStatusIcon,
    hasPendingSave,

    // Methods
    triggerSave,
    forceSave,
    cancelSave,
    enable,
    disable,
    reset,
    getTimeSinceLastSave
  };
}
