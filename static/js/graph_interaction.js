function handleScoreHistogramClick(minScore, maxScore) {
    let current_filters=extractFilterValues();
    redirect(current_filters);
}

function extractFilterValues() {
    let current_filters={}

    current_filters["min_score"] = document.getElementById("min-score-input").value
    current_filters["max_score"] = document.getElementById("max-score-input").value
    
    current_filters["year"] = document.getElementById("yearSelect").value
    current_filters["season"] = document.getElementById("seasonSelect").value

    let genres = []
    document.querySelectorAll('input[name="genres"]').forEach(genre => {
        if (genre.checked) {
            genres.push(genre.value)
        }
    })
    current_filters["genres"] = genres

    let demographics = []
    document.querySelectorAll('input[name="demographics"]').forEach(demographic => {
        if (demographic.checked) {
            demographics.push(demographic.value)
        }
    })
    current_filters["demographics"] = demographics

    return current_filters
}

function redirect(current_filters) {
    let urlString="/home?"

    urlString += `min_score=${current_filters["min_score"]}&max_score=${current_filters["max_score"]}`
    urlString += `&year=${current_filters["year"]}&season=${current_filters["season"]}`
    
    current_filters["genres"].forEach(genre => {
        urlString += `&genre=${genre}`
    })
    current_filters["demographics"].forEach(demographic => {
        urlString += `&demographic=${demographic}`
    })
    window.location.href = urlString
}