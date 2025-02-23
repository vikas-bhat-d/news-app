import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [news, setNews] = useState([]);
  const API_URL = "http://localhost:5001/news?limit=10";

  useEffect(() => {
    axios
      .get(API_URL)
      .then((response) => setNews(response.data.news))
      .catch((error) => console.error("Error fetching news:", error));
  }, []);

  return (
    <div className="app">
      <h1 className="title">Latest News</h1>
      <div className="news-container">
        {news.length === 0 ? (
          <p className="loading">Fetching news...</p>
        ) : (
          news.map((article, index) => (
            <div key={index} className="news-card">
              <h2>{article.title}</h2>
              <img src={article.image_url} alt="" />
              <p>{article.description || "No description available"}</p>
              <a href={article.url} target="_blank" rel="noopener noreferrer">
                Read More
              </a>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
