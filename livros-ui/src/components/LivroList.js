import { useEffect, useState } from 'react';
import { getLivros, deleteLivro } from '../services/api';
import { useNavigate } from 'react-router-dom';

const LivroList = () => {
    const [livros, setLivros] = useState([]);
    const navigate = useNavigate();

    const loadLivros = async () => {
        const data = await getLivros();
        setLivros(data);
    };

    const handleDelete = async (id) => {
        await deleteLivro(id);
        loadLivros();
    };

    useEffect(() => {
        loadLivros();
    }, []);

    return (
        <div>
            <h2>📚 Catálogo de Livros</h2>
            <button className="add-button" onClick={() => navigate('/livro')}>
                ➕ Adicionar Livro
            </button>
            
            <ul>
                {livros.map((livro) => (
                    <li key={livro.id}>
                        <span>📖 {livro.nome} <br></br> by <br></br> ✍️ {livro.autor}</span>
                        <div className="actions">
                            <button className="edit-button" onClick={() => navigate(`/livro/${livro.id}`)}>✏️ Editar</button>
                            <button className="delete-button" onClick={() => handleDelete(livro.id)}>🗑 Excluir</button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default LivroList;
