<script lang="ts">
  import { fade, slide, scale } from "svelte/transition";
  import FileUploader from "../components/FileUploader.svelte";
  import Footer from "../layout/Footer.svelte";
  import { uploadFile } from "../services/FileUpload";
  import { onMount } from "svelte";
  import SvelteMarkdown from "svelte-markdown";
  import Header from "../layout/Header.svelte";

  let keyPoints: string | null = $state<string>("");
  let error: string | null = $state<string | null>(null);
  let loading: boolean = $state<boolean>(false);
  let uploadSuccess: boolean = $state<boolean>(false);
  let typedResponse: string = $state<string>("");
  let typingInterval: ReturnType<typeof setInterval> | null = null;

  // Restore from localStorage on mount
  onMount(() => {
    const savedKeyPoints = localStorage.getItem("keyPoints");
    keyPoints = savedKeyPoints;
    error = localStorage.getItem("error");
    uploadSuccess = !!savedKeyPoints;

    if (savedKeyPoints) typedResponse = savedKeyPoints;

    return () => {
      if (typingInterval) clearInterval(typingInterval);
    };
  });

  const handleFileSelected = async (event: CustomEvent) => {
    const file = event.detail.file as File;
    if (file) {
      keyPoints = null;
      typedResponse = "";
      error = null;
      loading = true;
      uploadSuccess = false;

      try {
        const data: any = await uploadFile(file);
        if (data?.key_points) {
          keyPoints = data.key_points;
          error = null;
          uploadSuccess = true;

          // Start typing effect
          startTypingEffect(data.key_points);
        } else {
          keyPoints = null;
          error = data.message || "No key points found.";
          uploadSuccess = false;
        }
      } catch (err: any) {
        keyPoints = null;
        error = err?.message || "Upload failed.";
        uploadSuccess = false;
      } finally {
        loading = false;
        localStorage.setItem("keyPoints", keyPoints || "");
        localStorage.setItem("error", error || "");
      }
    }
  };

  const startTypingEffect = (text: string) => {
    if (typingInterval) clearInterval(typingInterval);

    let index = 0;
    typedResponse = "";

    typingInterval = setInterval(() => {
      if (index < text.length) {
        typedResponse = text.substring(0, index + 1);
        index++;
      } else {
        if (typingInterval) clearInterval(typingInterval);
      }
    }, 10);
  };

  const resetUploader = () => {
    keyPoints = null;
    typedResponse = "";
    error = null;
    uploadSuccess = false;
    localStorage.removeItem("keyPoints");
    localStorage.removeItem("error");
  };
</script>

<div
  class="min-h-screen bg-light-cream p-6 flex flex-col items-center justify-center"
>
  <div class="w-full max-w-6xl mx-auto">
    <Header />
    <div class="flex flex-col md:flex-row gap-8 items-start justify-center">
      <!-- Left: Upload Section -->
      <div class="flex-1 w-full max-w-md">
        {#if !uploadSuccess}
          <FileUploader on:fileSelected={handleFileSelected} {loading} />
        {:else}
          <div
            in:scale={{ duration: 300 }}
            class="card w-full p-8 flex flex-col items-center justify-center gap-6"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-16 w-16 text-green-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              />
            </svg>
            <h3 class="text-2xl font-bold text-center">
              Document Processed Successfully!
            </h3>
            <p class="text-center text-text-dark/80">
              Your key insights are ready. Want to analyze another document?
            </p>
            <button
              onclick={resetUploader}
              class="btn btn-secondary mt-4 flex items-center gap-2"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              Analyze Another Document
            </button>
          </div>
        {/if}
      </div>

      <!-- Right: Results -->
      <div class="flex-1 w-full max-w-2xl">
        {#if loading}
          <div
            transition:fade
            class="card w-full p-6 flex flex-col items-center justify-center gap-4 mt-6"
          >
            <div class="animate-pulse flex flex-col w-full gap-3">
              <div class="h-6 bg-gray-200 rounded w-1/3"></div>
              <div class="h-4 bg-gray-200 rounded w-full"></div>
              <div class="h-4 bg-gray-200 rounded w-5/6"></div>
              <div class="h-4 bg-gray-200 rounded w-2/3"></div>
            </div>
            <div class="mt-4 w-full flex justify-center">
              <div
                class="h-2 w-24 bg-vibrant-orange/20 rounded-full animate-pulse"
              ></div>
            </div>
          </div>
        {/if}
        {#if error}
          <div
            transition:slide
            class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-6"
          >
            <div class="flex items-start gap-3">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6 flex-shrink-0"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
              <div>
                <p class="font-medium">Error Processing Document</p>
                <p class="mt-1">{error}</p>
                <button
                  onclick={resetUploader}
                  class="mt-3 text-vibrant-orange font-medium hover:underline flex items-center gap-1"
                >
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
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    />
                  </svg>
                  Try again
                </button>
              </div>
            </div>
          </div>
        {/if}

        {#if typedResponse || (keyPoints && !loading)}
          <div transition:slide class="card w-full p-6 relative">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-2xl font-bold text-text-dark">Key Insights</h2>
              <span class="highlight-badge flex items-center gap-1">
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
                    d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                  />
                </svg>
                AI Generated
              </span>
            </div>

            <div class="prose max-w-none text-text-dark min-h-[200px]">
              {#if typedResponse}
                <SvelteMarkdown source={typedResponse} />
              {:else}
                <SvelteMarkdown source={keyPoints} />
              {/if}
            </div>

            {#if loading && !typedResponse}
              <div
                class="absolute inset-0 bg-light-cream/80 flex items-center justify-center"
              >
                <div class="text-center">
                  <div
                    class="inline-block animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-vibrant-orange"
                  ></div>
                  <p class="mt-3 font-medium">Analyzing your document...</p>
                </div>
              </div>
            {/if}
          </div>
        {:else if !error}
          <div
            transition:fade
            class="card w-full p-8 flex flex-col items-center justify-center gap-4 text-center min-h-[200px]"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-12 w-12 text-text-dark/30"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 class="text-xl font-bold text-text-dark">Upload a Document</h3>
            <p class="text-text-dark/60 max-w-md">
              Get AI-powered insights from your PDF, DOCX, or TXT files. Upload
              a document to get started.
            </p>
          </div>
        {/if}
      </div>
    </div>
    <Footer />
  </div>
</div>
