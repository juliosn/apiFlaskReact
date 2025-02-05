import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getLivros, addLivro, updateLivro } from '../services/api';

const LivroForm = () => {
    const navigate = useNavigate();
    const { id } = useParams();
    const [livro, setLivro] = useState({ nome: '', autor: '', ano: '', preco: '' });

    useEffect(() => {
        if (id) {
            const fetchLivro = async () => {
                const livros = await getLivros();
                const livroEncontrado = livros.find(l => l.id === parseInt(id));
                if (livroEncontrado) {
                    setLivro(livroEncontrado);
                }
            };
            fetchLivro();
        }
    }, [id]);

    const handleChange = (e) => {
        setLivro({ ...livro, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (id) {
            await updateLivro(id, livro);
        } else {
            await addLivro(livro);
        }
        navigate('/'); // 🔙 Voltar para a tela principal
    };

    return (
        <div>
            <h2>{id ? 'Editar Livro' : 'Adicionar Livro'}</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="nome" placeholder="Nome" value={livro.nome} onChange={handleChange} required />
                <input type="text" name="autor" placeholder="Autor" value={livro.autor} onChange={handleChange} required />
                <input type="number" name="ano" placeholder="Ano" value={livro.ano} onChange={handleChange} required />
                <input type="number" step="0.01" name="preco" placeholder="Preço" value={livro.preco} onChange={handleChange} required />
                <button type="submit">{id ? 'Atualizar' : 'Adicionar'}</button>
            </form>
        </div>
    );
};

export default LivroForm;
