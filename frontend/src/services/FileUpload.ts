import { API } from "./_axios";

export const uploadFile = async (file: File): Promise<string> => {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await API.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            withCredentials: true,
        });
        return response.data;
    } catch (error) {
        console.error(`Error uploading file: ${error}`);
        throw error;
    }
}