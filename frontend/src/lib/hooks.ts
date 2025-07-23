import { createMutation } from "@tanstack/svelte-query";
import { uploadFile } from "../services/FileUpload";

export const useFileUpload = () => {
    return createMutation({
        mutationFn: uploadFile,
    });
};