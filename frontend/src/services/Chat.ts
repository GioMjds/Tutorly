import { API } from "./_axios";

export const getChat = async () => {
    try {
        const response = await API.get('/chat');
        return response.data;
    } catch (error) {
        console.error(`Error fetching chat: ${error}`);
        throw error;
    }
}