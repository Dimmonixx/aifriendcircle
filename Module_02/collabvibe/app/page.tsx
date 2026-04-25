'use client';

import { useState } from 'react';

interface Idea {
  id: string;
  text: string;
  author: string;
  date: string;
  likes: number;
}

interface User {
  name: string;
  email: string;
}

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login');
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [registerName, setRegisterName] = useState('');
  const [registerEmail, setRegisterEmail] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [authError, setAuthError] = useState('');
  
  const [ideas, setIdeas] = useState<Idea[]>([
    {
      id: '1',
      text: 'Реализовать систему проверки кода на базе ИИ для автоматической проверки качества и предложений улучшений',
      author: 'Алексей Чен',
      date: '2024-04-22',
      likes: 12
    },
    {
      id: '2',
      text: 'Создать дашборд команды с метриками проектов в реальном времени и аналитикой производительности команды',
      author: 'Мария Родригес',
      date: '2024-04-21',
      likes: 8
    },
    {
      id: '3',
      text: 'Разработать конвейер автоматического тестирования с параллельным выполнением и детальной отчетностью',
      author: 'Давид Ким',
      date: '2024-04-20',
      likes: 15
    },
    {
      id: '4',
      text: 'Спроектировать библиотеку UI компонентов с приоритетом мобильных устройств и поддержкой темной темы',
      author: 'Сара Джонсон',
      date: '2024-04-19',
      likes: 20
    },
    {
      id: '5',
      text: 'Разработать функции совместной работы в реальном времени с живыми курсорами и индикаторами присутствия',
      author: 'Том Уилсон',
      date: '2024-04-18',
      likes: 18
    }
  ]);

  const [newIdea, setNewIdea] = useState('');
  const [author, setAuthor] = useState('');

  const addIdea = () => {
    if (newIdea.trim() && author.trim()) {
      const idea: Idea = {
        id: Date.now().toString(),
        text: newIdea.trim(),
        author: author.trim(),
        date: new Date().toISOString().split('T')[0],
        likes: 0
      };
      setIdeas([idea, ...ideas]);
      setNewIdea('');
      setAuthor('');
    }
  };

  const likeIdea = (id: string) => {
    setIdeas(ideas.map(idea => 
      idea.id === id ? { ...idea, likes: idea.likes + 1 } : idea
    ));
  };

  const handleLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: loginEmail,
          password: loginPassword,
        }),
      });
      
      if (response.ok) {
        // Get user info from users list to get name
        const usersResponse = await fetch('http://localhost:8000/users');
        const usersData = await usersResponse.json();
        const currentUser = usersData.users.find((u: User) => u.email === loginEmail);
        
        if (currentUser) {
          setUser(currentUser);
          setAuthError('');
          setLoginEmail('');
          setLoginPassword('');
        }
      } else {
        setAuthError('Неверный email или пароль');
      }
    } catch (error) {
      setAuthError('Ошибка подключения к серверу');
    }
  };

  const handleRegister = async () => {
    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: registerName,
          email: registerEmail,
          password: registerPassword,
        }),
      });
      
      if (response.ok) {
        setUser({ name: registerName, email: registerEmail });
        setAuthError('');
        setRegisterName('');
        setRegisterEmail('');
        setRegisterPassword('');
      } else {
        setAuthError('Ошибка регистрации');
      }
    } catch (error) {
      setAuthError('Ошибка подключения к серверу');
    }
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            CollabVibe - Доска идей
          </h1>
          <p className="text-gray-400 text-lg">Делитесь идеями и сотрудничайте с командой</p>
          
          {/* User Authentication */}
          {!user ? (
            <div className="mt-8 max-w-md mx-auto">
              <div className="bg-gray-800 rounded-2xl p-6 border border-purple-500/20">
                {/* Tabs */}
                <div className="flex mb-6">
                  <button
                    onClick={() => setActiveTab('login')}
                    className={`flex-1 py-2 px-4 rounded-l-lg font-medium transition-all ${
                      activeTab === 'login'
                        ? 'bg-purple-500 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    Войти
                  </button>
                  <button
                    onClick={() => setActiveTab('register')}
                    className={`flex-1 py-2 px-4 rounded-r-lg font-medium transition-all ${
                      activeTab === 'register'
                        ? 'bg-purple-500 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    Зарегистрироваться
                  </button>
                </div>

                {/* Error Message */}
                {authError && (
                  <div className="mb-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-300 text-sm">
                    {authError}
                  </div>
                )}

                {/* Login Form */}
                {activeTab === 'login' && (
                  <div className="space-y-4">
                    <input
                      type="email"
                      placeholder="Email..."
                      value={loginEmail}
                      onChange={(e) => setLoginEmail(e.target.value)}
                      className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    />
                    <input
                      type="password"
                      placeholder="Пароль..."
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                      className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    />
                    <button
                      onClick={handleLogin}
                      className="w-full px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 active:scale-95"
                    >
                      Войти
                    </button>
                  </div>
                )}

                {/* Register Form */}
                {activeTab === 'register' && (
                  <div className="space-y-4">
                    <input
                      type="text"
                      placeholder="Имя..."
                      value={registerName}
                      onChange={(e) => setRegisterName(e.target.value)}
                      className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    />
                    <input
                      type="email"
                      placeholder="Email..."
                      value={registerEmail}
                      onChange={(e) => setRegisterEmail(e.target.value)}
                      className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    />
                    <input
                      type="password"
                      placeholder="Пароль..."
                      value={registerPassword}
                      onChange={(e) => setRegisterPassword(e.target.value)}
                      className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    />
                    <button
                      onClick={handleRegister}
                      className="w-full px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 active:scale-95"
                    >
                      Зарегистрироваться
                    </button>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="mt-8 flex items-center justify-center gap-4">
              <span className="text-purple-400 font-medium text-lg">Привет, {user.name}!</span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-all"
              >
                Выйти
              </button>
            </div>
          )}
        </header>

        {/* Add Idea Section */}
        {user && (
          <section className="mb-12">
            <div className="bg-gray-800 rounded-2xl p-6 border border-purple-500/20">
              <div className="space-y-4">
                <input
                  type="text"
                  placeholder="Ваше имя..."
                  value={author}
                  onChange={(e) => setAuthor(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
                <textarea
                  placeholder="Поделитесь своей идеей..."
                  value={newIdea}
                  onChange={(e) => setNewIdea(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none h-32"
                />
                <button
                  onClick={addIdea}
                  className="w-full px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 active:scale-95"
                >
                  Добавить идею
                </button>
              </div>
            </div>
          </section>
        )}

        {/* Ideas Grid */}
        <section>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {ideas.map((idea) => (
              <div
                key={idea.id}
                className="bg-gray-800 rounded-xl p-6 border border-purple-500/20 hover:border-purple-500/40 transition-all hover:shadow-lg hover:shadow-purple-500/20"
              >
                <div className="mb-4">
                  <p className="text-gray-100 mb-4 leading-relaxed">{idea.text}</p>
                </div>
                
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <p className="text-purple-400 font-medium">{idea.author}</p>
                    <p className="text-gray-500 text-sm">{idea.date}</p>
                  </div>
                  <button
                    onClick={() => likeIdea(idea.id)}
                    className="flex items-center gap-2 px-3 py-1 bg-gray-700 rounded-lg hover:bg-purple-500/20 transition-all group"
                  >
                    <span className="text-pink-400 group-hover:text-pink-300">heart:</span>
                    <span className="text-gray-300 group-hover:text-gray-200">{idea.likes}</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-500">
          <p>Создано с помощью Next.js и Tailwind CSS</p>
        </footer>
      </div>
    </div>
  );
}
