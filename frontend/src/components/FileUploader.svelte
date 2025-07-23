<script lang="ts">
  import { createEventDispatcher } from "svelte";
  export let loading: boolean = false;
  let file: File | null = null;
  const dispatch = createEventDispatcher();

  const handleFileChange = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      file = input.files[0];
      dispatch("fileSelected", { file });
    }
  }

  const handleUpload = () => {
    if (file) dispatch("fileSelected", { file });
  }
</script>

<div class="card w-full max-w-md mx-auto transition-all duration-300">
  <div class="flex flex-col items-center gap-4">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-text-dark mb-2">
        Upload Your Document
      </h2>
      <p class="text-sm text-gray-600">
        Supported formats: PDF, DOCX, TXT (Max 10MB)
      </p>
    </div>

    <label
      class="w-full border-2 border-dashed border-border-light rounded-rounded-box p-8 flex flex-col items-center justify-center cursor-pointer hover:border-vibrant-orange transition-colors duration-200 {loading
        ? 'opacity-50'
        : ''}"
    >
      <input
        type="file"
        accept=".pdf,.docx,.txt"
        class="hidden"
        on:change={handleFileChange}
        disabled={loading}
      />
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-12 w-12 text-vibrant-orange mb-3"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
        />
      </svg>
      <span class="font-medium text-text-dark">
        {#if file}
          {file.name}
        {:else}
          Click to select a file
        {/if}
      </span>
      <span class="text-xs text-gray-500 mt-1">
        {#if file}
          {(file.size / 1024 / 1024).toFixed(2)} MB
        {:else}
          or drag and drop
        {/if}
      </span>
    </label>

    <button
      class="btn btn-primary cursor-pointer w-full mt-4 flex items-center justify-center gap-2"
      on:click={handleUpload}
      disabled={!file || loading}
    >
      {#if loading}
        <svg
          class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        Processing...
      {:else}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
        Analyze Document
      {/if}
    </button>
  </div>
</div>
