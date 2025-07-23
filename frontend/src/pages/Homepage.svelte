<script lang="ts">
    import { createQuery } from "@tanstack/svelte-query";
    import { getChat } from "../services/Chat";

    const query = createQuery({
        queryKey: ['chat'],
        queryFn: getChat,
    })
</script>

<div>
    {#if $query.isLoading}
        <p>Loading...</p>
    {:else if $query.isError}
        <p>Error fetching chat data</p>
    {:else if $query.isSuccess}
        <h1 class="text-2xl">{$query.data.message}</h1>
    {/if}
</div>