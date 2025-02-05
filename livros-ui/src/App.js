import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LivroList from './components/LivroList';
import './App.css';
import LivroForm from './components/LivroForm';

function App() {
    return (
        <Router>
            <div className="App">
                <h1>Gerenciador de Livros</h1>
                <Routes>
                    <Route path="/" element={<LivroList />} />
                    <Route path="/livro/:id?" element={<LivroForm />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
