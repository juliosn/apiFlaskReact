import axios from 'axios';

const API_URL = 'http://localhost:5001/api/v1/livros';

export const getLivros = async () => {
    const response = await axios.get(API_URL);
    return response.data;
};

export const addLivro = async (livro) => {
    const response = await axios.post(API_URL, livro);
    return response.data;
};

export const updateLivro = async (id, livro) => {
    const response = await axios.put(`${API_URL}/${id}`, livro);
    return response.data;
};

export const deleteLivro = async (id) => {
    await axios.delete(`${API_URL}/${id}`);
};
