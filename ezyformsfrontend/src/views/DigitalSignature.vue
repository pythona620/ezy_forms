<template>
  <div class="signature-container">
    <!-- Digital Signature Canvas -->
    <div class="signature-section mb-3">
      <!-- <label class="font-13 mb-2">Digital Signature</label> -->
      <div class="signature-canvas-container">
        <canvas
          ref="signatureCanvas"
          class="signature-canvas"
          :class="{ 'is-invalid': errors.signature }"
          @mousedown="startDrawing"
          @mousemove="draw"
          @mouseup="stopDrawing"
          @mouseleave="stopDrawing"
          @touchstart="startDrawing"
          @touchmove="draw"
          @touchend="stopDrawing"
        ></canvas>
        <div class="signature-placeholder" v-if="!hasSignature">
          Sign here
        </div>
      </div>
      
      <!-- Signature Controls -->
      <div class="signature-controls  mt-2">
        <button
          type="button"
          class="btn btn-outline-secondary font-13 me-2"
          @click="clearSignature"
        >
          Clear
        </button>
        <!-- <button
          type="button"
          class="save-btn"
          @click="saveSignature"
        >
          Save Signature
        </button> -->
        <!-- <button
          type="button"
          class="btn btn-outline-info btn-sm"
          @click="toggleSignatureModal"
        >
          Upload Image
        </button> -->
      </div>
      
      <!-- Error Message -->
      <div class="invalid-feedback font-11 mt-1" v-if="errors.signature">
        {{ errors.signature }}
      </div>
    </div>

    <!-- Signature Preview -->
    <!-- <div class="signature-preview mb-3" v-if="signatureDataUrl">
      <label class="font-13 mb-2">Signature Preview</label>
      <div class="preview-container">
        <img :src="signatureDataUrl" alt="Signature Preview" class="signature-image" />
        <button
          type="button"
          class="btn btn-sm btn-outline-danger position-absolute top-0 end-0 m-1"
          @click="removeSignature"
        >
          ×
        </button>
      </div>
    </div> -->

    <!-- Upload Modal -->
    <div class="modal fade" id="signatureUploadModal" tabindex="-1" ref="signatureModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Upload Signature</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input
              type="file"
              ref="fileInput"
              class="form-control"
              accept="image/*"
              @change="handleFileUpload"
            />
            <small class="text-muted">
              Supported formats: PNG, JPG, JPEG (Max size: 2MB)
            </small>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DigitalSignature',
  data() {
    return {
      isDrawing: false,
      canvas: null,
      ctx: null,
      signatureDataUrl: null,
      hasSignature: false,
      errors: {
        signature: null
      },
      // Drawing settings
      lineWidth: 2,
      strokeStyle: '#000000'
    };
  },
  
  mounted() {
    this.initializeCanvas();
  },
  
  methods: {
    initializeCanvas() {
      this.canvas = this.$refs.signatureCanvas;
      this.ctx = this.canvas.getContext('2d');
      
      // Set canvas size
      const container = this.canvas.parentElement;
      this.canvas.width = container.clientWidth;
      this.canvas.height = 200;
      
      // Set drawing style
      this.ctx.lineWidth = this.lineWidth;
      this.ctx.strokeStyle = this.strokeStyle;
      this.ctx.lineCap = 'round';
      this.ctx.lineJoin = 'round';
      
      // Prevent scrolling when touching the canvas
      this.canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
      });
      
      this.canvas.addEventListener('touchmove', (e) => {
        e.preventDefault();
      });
    },
    
    getCoordinates(event) {
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.canvas.width / rect.width;
      const scaleY = this.canvas.height / rect.height;
      
      if (event.touches && event.touches[0]) {
        return {
          x: (event.touches[0].clientX - rect.left) * scaleX,
          y: (event.touches[0].clientY - rect.top) * scaleY
        };
      } else {
        return {
          x: (event.clientX - rect.left) * scaleX,
          y: (event.clientY - rect.top) * scaleY
        };
      }
    },
    
    startDrawing(event) {
      this.isDrawing = true;
      const coordinates = this.getCoordinates(event);
      
      this.ctx.beginPath();
      this.ctx.moveTo(coordinates.x, coordinates.y);
      
      this.hasSignature = true;
      this.clearError();
    },
    
    draw(event) {
      if (!this.isDrawing) return;
      
      const coordinates = this.getCoordinates(event);
      this.ctx.lineTo(coordinates.x, coordinates.y);
      this.ctx.stroke();
    },
    
    stopDrawing() {
      if (!this.isDrawing) return;
      this.isDrawing = false;
      this.ctx.closePath();
    },
    
    clearSignature() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.hasSignature = false;
      this.signatureDataUrl = null;
      this.clearError();
      this.$emit('signature-cleared');
    },
    
    saveSignature() {
      if (!this.hasSignature && !this.signatureDataUrl) {
        this.setError('Please provide a signature');
        return;
      }
      
      // Convert canvas to data URL
      const dataUrl = this.canvas.toDataURL('image/png');
      this.signatureDataUrl = dataUrl;
      
      // Emit the signature data
      this.$emit('signature-saved', {
        dataUrl: dataUrl,
        blob: this.dataURLtoBlob(dataUrl)
      });
      
      this.clearError();
      
      // Show success message
      this.$emit('signature-success', 'Signature saved successfully!');
    },
    
    removeSignature() {
      this.signatureDataUrl = null;
      this.clearSignature();
      this.$emit('signature-removed');
    },
    
    // toggleSignatureModal() {
    //   const modal = new bootstrap.Modal(this.$refs.signatureModal);
    //   modal.show();
    // },
    
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      // Validate file type
      if (!file.type.startsWith('image/')) {
        this.setError('Please select a valid image file');
        return;
      }
      
      // Validate file size (2MB max)
      if (file.size > 2 * 1024 * 1024) {
        this.setError('File size must be less than 2MB');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          // Clear canvas and draw the uploaded image
          this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
          
          // Calculate scaling to fit image in canvas
          const scale = Math.min(
            this.canvas.width / img.width,
            this.canvas.height / img.height
          );
          
          const x = (this.canvas.width - img.width * scale) / 2;
          const y = (this.canvas.height - img.height * scale) / 2;
          
          this.ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
          
          this.hasSignature = true;
          this.signatureDataUrl = this.canvas.toDataURL('image/png');
          
          // Close modal
          const modal = bootstrap.Modal.getInstance(this.$refs.signatureModal);
          modal.hide();
          
          this.clearError();
          this.$emit('signature-uploaded', {
            dataUrl: this.signatureDataUrl,
            blob: this.dataURLtoBlob(this.signatureDataUrl)
          });
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
      
      // Clear file input
      event.target.value = '';
    },
    
    dataURLtoBlob(dataurl) {
      const arr = dataurl.split(',');
      const mime = arr[0].match(/:(.*?);/)[1];
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new Blob([u8arr], { type: mime });
    },
    
    setError(message) {
      this.errors.signature = message;
    },
    
    clearError() {
      this.errors.signature = null;
    },
    
    validateSignature() {
      if (!this.hasSignature && !this.signatureDataUrl) {
        this.setError('Signature is required');
        return false;
      }
      this.clearError();
      return true;
    },
    
    getSignatureData() {
      return {
        hasSignature: this.hasSignature || !!this.signatureDataUrl,
        dataUrl: this.signatureDataUrl || this.canvas.toDataURL('image/png'),
        blob: this.signatureDataUrl ? 
          this.dataURLtoBlob(this.signatureDataUrl) : 
          this.dataURLtoBlob(this.canvas.toDataURL('image/png'))
      };
    }
  }
};
</script>

<style scoped>
.signature-container {
  width: 100%;
}

.signature-canvas-container {
  position: relative;
  border: 2px dashed #ddd;
  border-radius: 8px;
  background-color: #fafafa;
  overflow: hidden;
}

.signature-canvas {
  display: block;
  width: 100%;
  height: 90px;
  cursor: crosshair;
  background-color: white;
}

.signature-canvas.is-invalid {
  border-color: #dc3545;
}

.signature-placeholder {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #999;
  font-size: 16px;
  pointer-events: none;
  z-index: 1;
}

.signature-controls {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.signature-preview {
  position: relative;
}

.preview-container {
  position: relative;
  display: inline-block;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px;
  background-color: white;
}

.signature-image {
  max-width: 200px;
  max-height: 100px;
  border-radius: 4px;
}

.font-13 {
  font-size: 13px;
}

.font-11 {
  font-size: 11px;
}

.invalid-feedback {
  display: block;
  color: #dc3545;
}

.save-btn{
    border: 1px solid #dc3545;
    color: #dc3545;
    border-radius: 5px;
    background: transparent;
    font-size: 13px;
}

.save-btn:hover{
    border: 1px solid #dc3545;
    color: white;
    border-radius: 5px;
    background: #dc3545;
    font-size: 13px;
}

/* Responsive design */
@media (max-width: 576px) {
  .signature-controls {
    flex-direction: column;
  }
  
  .signature-controls .btn {
    width: 100%;
  }
}
</style>