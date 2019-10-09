let URL_API= 'https://api.themoviedb.org/3/account/{account_id}/favorite/movies?api_key=516adf1e1567058f8ecbf30bf2eb9378&session_id=c8e2bd462c246b141fd19ddba2e5f091f6f8aedb&language=en-US&sort_by=created_at.asc&page=1';
URL_API= 'https://api.themoviedb.org/3/list/15570?api_key=516adf1e1567058f8ecbf30bf2eb9378&language=en-US';
let movieList = [];
let i=0;
const card = document.querySelector('.content');
let ca = document.createElement('a');
let img = document.createElement('img');

function mapCards(movies){
  //console.log(movie);
  const html = movies.map(movie => {
    let poster = movie.poster_path;
    //console.log(poster);
    let title = movie.title || movie.name;
    let isMovieOrTv=(movie.title)?'movie':'tv';
    return `
      <a target="_blank"class="card" href="https://www.themoviedb.org/movie/${movie.id}">
    <div class="front" style="background-image: url(//image.tmdb.org/t/p/original${movie.poster_path});"> 
      <p>${title}</p>
    </div>
    <div class="back">
      <div>
        <p class="overview">${movie.overview}</p>
        <button class="button">Details</button>
      </div>
    </div>
  </a>
    `;
  }).join('');
  card.innerHTML= 
    `<h1 class="heading">Card Flip - Movies</h1>
  <p class="description">Hover over a card to flip it.</p>`;
  card.innerHTML+= html;
}

fetch(URL_API, {
  method: "GET",
  headers: {
    'Content-Type': 'application/json' 
  }
})
  .then(resp => resp.json())
  .then(data => {
    movieList=((data.items) || data.results);
    mapCards(movieList);

  })
  .catch((err) => {
    console.log(err);  
  })
