import { useState } from 'react';

function MiniApp() {
    const [activeTab, setActiveTab] = useState('home');
    const [savedNews, setSavedNews] = useState([]);

    const newsData = [
        {
            title: "Новий прорив у технології штучного інтелекту",
            source: "Tech News",
            time: "15 хв тому",
            category: "Технології",
            image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=200&fit=crop"
        },
        {
            title: "Економічні показники демонструють зростання",
            source: "Економічна правда",
            time: "1 год тому",
            category: "Економіка",
            image: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&h=200&fit=crop"
        },
        {
            title: "Спортивні досягнення українських атлетів",
            source: "Спорт24",
            time: "2 год тому",
            category: "Спорт",
            image: "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&h=200&fit=crop"
        },
        {
            title: "Нові відкриття в медицині обіцяють революцію",
            source: "Медична газета",
            time: "3 год тому",
            category: "Здоров'я",
            image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400&h=200&fit=crop"
        }
    ];

    const trendingTopics = [
        "Технології",
        "Політика",
        "Економіка",
        "Спорт",
        "Культура"
    ];

    const NewsCard = () => (
        <div className="bg-white rounded-lg overflow-hidden shadow-sm mb-3 hover:shadow-md transition-shadow">
            <img 
                className="w-full h-40 object-cover"
            />
            <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded">
                        {} 
                    </span>
                    <span className="text-xs text-gray-500">{} </span>
                </div>
                <h3 className="font-semibold text-gray-800 mb-2 leading-snug">
                    {} 
                </h3>
                <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-600">{} </span>
                    <button 
                        className="p-1.5 hover:bg-gray-100 rounded-full transition-colors"
                    >
                        <svg 
                            width="18" 
                            height="18" 
                            viewBox="0 0 24 24" 
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    );

    return (
        <div className="max-w-md mx-auto bg-gray-50 min-h-screen flex flex-col">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-500 text-white p-4 shadow-lg">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/>
                            <path d="M18 14h-8"/>
                            <path d="M15 18h-5"/>
                            <path d="M10 6h8v4h-8V6Z"/>
                        </svg>
                        <h1 className="text-xl font-bold">Новини</h1>
                    </div>
                    <button className="p-2 hover:bg-blue-700 rounded-full transition-colors">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="3"/>
                            <path d="M12 1v6m0 6v6m9-9h-6m-6 0H3"/>
                        </svg>
                    </button>
                </div>
                
                {/* Search Bar */}
                <div className="relative">
                    <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="11" cy="11" r="8"/>
                        <path d="m21 21-4.35-4.35"/>
                    </svg>
                    <input 
                        type="text"
                        placeholder="Пошук новин..."
                        className="w-full pl-10 pr-4 py-2 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-300"
                    />
                </div>
            </div>

            {/* Trending Topics */}
            {activeTab === 'home' && (
                <div className="px-4 py-3 bg-white border-b">
                    <div className="flex items-center gap-2 mb-2">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f97316" strokeWidth="2">
                            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
                            <polyline points="17 6 23 6 23 12"/>
                        </svg>
                        <h2 className="font-semibold text-gray-700">Популярні теми</h2>
                    </div>
                    <div className="flex gap-2 overflow-x-auto pb-2">
                        {trendingTopics.map((topic, i) => (
                            <button 
                                key={i}
                                className="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm rounded-full whitespace-nowrap transition-colors"
                            >
                                {topic}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4">
                {activeTab === 'home' && (
                    <div>
                        <h2 className="text-lg font-bold text-gray-800 mb-3">Останні новини</h2>
                        {newsData.map((news, i) => (
                            <NewsCard key={i} />
                        ))}
                    </div>
                )}
            </div>

            {/* Bottom Navigation */}
            <div className="bg-white border-t shadow-lg">
                <div className="flex justify-around p-2">
                    <button 
                        onClick={() => setActiveTab('home')}
                        className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-colors ${
                            activeTab === 'home' 
                                ? 'text-blue-600 bg-blue-50' 
                                : 'text-gray-600 hover:bg-gray-50'
                        }`}
                    >
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                            <polyline points="9 22 9 12 15 12 15 22"/>
                        </svg>
                        <span className="text-xs font-medium">Головна</span>
                    </button>
                    
                    <button 
                        onClick={() => setActiveTab('saved')}
                        className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-colors ${
                            activeTab === 'saved' 
                                ? 'text-blue-600 bg-blue-50' 
                                : 'text-gray-600 hover:bg-gray-50'
                        }`}
                    >
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                        </svg>
                        <span className="text-xs font-medium">Збережені</span>
                    </button>
                </div>
            </div>
        </div>
    );
}

export default MiniApp;