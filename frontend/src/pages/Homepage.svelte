<script lang="ts">
  import { createMutation } from "@tanstack/svelte-query";
  import { fade, slide } from "svelte/transition";
  import Footer from "../layout/Footer.svelte";
  import FileUploader from "../components/FileUploader.svelte";
  import { uploadFile } from "../services/FileUpload";

  let keyPoints: string | null = null;
  let error: string | null = null;

  const fileUploadMutation = createMutation({
    mutationFn: uploadFile,
    onSuccess: (data: any) => {
      if (data.key_points) {
        keyPoints = data.key_points;
        error = null;
      } else {
        keyPoints = null;
        error = data.message || "No key points found.";
      }
    },
    onError: (err: any) => {
      keyPoints = null;
      error = err?.message || "Upload failed.";
    },
  });

  const handleFileSelected = (event: CustomEvent) => {
    const file = event.detail.file as File;
    if (file) {
      keyPoints = null;
      error = null;
      $fileUploadMutation.mutate(file);
    }
  }
</script>

<div
  class="flex flex-col items-center justify-center min-h-screen bg-light-cream p-6"
>
  <div class="w-full max-w-4xl mx-auto space-y-8">
    <header class="text-center">
      <h1 class="text-4xl font-bold text-vibrant-orange mb-2">Tutorly AI</h1>
      <p class="text-lg text-text-dark/80 max-w-2xl mx-auto">
        Upload your study materials and get instant key points extraction
        powered by AI
      </p>
    </header>

    <FileUploader
      on:fileSelected={handleFileSelected}
      loading={$fileUploadMutation.isPending}
    />

    {#if $fileUploadMutation.isPending}
      <div
        transition:fade
        class="card w-full p-6 flex flex-col items-center justify-center gap-4"
      >
        <div class="animate-pulse flex flex-col w-full gap-3">
          <div class="h-6 bg-gray-200 rounded w-1/3"></div>
          <div class="h-4 bg-gray-200 rounded w-full"></div>
          <div class="h-4 bg-gray-200 rounded w-5/6"></div>
          <div class="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>
    {/if}
    {#if error}
      <div
        transition:slide
        class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg"
      >
        <p class="font-medium">Error:</p>
        <p>{error}</p>
      </div>
    {/if}
    {#if keyPoints}
      <div transition:slide class="card w-full p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold text-text-dark">Key Insights</h2>
          <span class="highlight-badge">AI Generated</span>
        </div>
        <div class="prose max-w-none text-text-dark">
          {#each keyPoints.split("\n") as paragraph}
            {#if paragraph.trim()}
              <p class="mb-4">{paragraph}</p>
            {/if}
          {/each}
        </div>
      </div>
    {/if}
    <Footer />
  </div>
</div>
