let modal = document.querySelector(".modal")
let showNotificationSetup = document.querySelectorAll(".popup")
let showDropdownElement = document.querySelectorAll('.dropdown')
let close = document.querySelector(".close-button")
let modalHeader = document.querySelector("#modal-header")
let modalValue = document.querySelector("#modal-value")
let chosenPercentageInput = document.querySelector("#percentage-value")
let notificationValue = document.querySelector("#modal-notification-value")
let addNotificationButton = document.querySelector("#add-notification")
let currentStockNumericValue = 0
let currentStockAbbreviation = ''
let currentPercentageNumericValue = 0
let currentStockName = ''

function toggleModal(event) {
    if (event.target.className === "far fa-bell fa-2x popup dumbbell") {
        renderStockInfo(event.target.id)
    }
    modal.classList.toggle("show-modal")
}

function toggleDropdown(event) {
    if (event.target.className === "far fa-chart-bar fa-2x dropdown") {
        renderChart(event.target.id)
    }
}

function windowOnClick(event) {
    
    if (event.target === modal) {
        toggleModal(event)
    }
}

// klikjac na miejsce poza modalem jest error
// tez jak zamyka sie okno to trzeba wyzerowac wartosc procentowa inputa i wartosc powiadomienia

function renderStockInfo(targetId) {
    let targetedStockFormatted = targetId.substring(13)
    let targetedStock = document.getElementById(targetedStockFormatted)

    let stockName = targetedStock.getElementsByClassName("stock-name")[0].innerText
    let stockValue = targetedStock.getElementsByClassName("stock-value")[0].innerText

    currentStockNumericValue = Number.parseFloat(stockValue.slice(0,-1))
    currentStockName = stockName
    currentStockAbbreviation = targetedStock.getElementsByClassName("stock-abbreviation")[0].innerText

    console.log(stockName, currentStockAbbreviation, stockValue)
    modalHeader.innerText = "Set up notification for " + stockName
    modalValue.innerText = "Current value: " + stockValue
}

async function renderChart(targetId) {
    let targetedStockName = targetId.toString().substring(6)
    let targetedStockContent = "chart-info-" + targetedStockName
    let targetedChartDiv = document.getElementById(targetedStockContent)
    let targetedStock = document.getElementById(targetedStockName)

    let graphExists = document.getElementById("graph-" + targetedStockName)
    if (graphExists !== null) {
        animateChartInfo(targetedStock, targetedChartDiv)
        return null
    }

    let graphDiv = createGraphDivWithId(targetedStockName)
    targetedChartDiv.insertAdjacentElement('afterbegin', graphDiv)

    requestGraphForStock(targetedStockName)
        .then(data => {
            let graph = JSON.parse(data.graph)
            Bokeh.embed.embed_item(graph, graphDiv.id)
        })
        .then(() => {
            animateChartInfo(targetedStock, targetedChartDiv)
        })
        .catch(error => {
            console.log(error)
        })

}

function createGraphDivWithId(stockName) {
    let graphDiv = document.createElement("div")
    graphDiv.id = "graph-" + stockName
    graphDiv.classList.add("graph-div")
    return graphDiv
}

function calculateNotificationValue(event) {

    if (event.code.startsWith("Digit") || event.code.startsWith("Numpad") || event.code.startsWith("Minus")) {
        setValidPercentageInput()
        setNotificationValue()
    }
}

function setValidPercentageInput() {
    let parsedValue = Number.parseFloat(chosenPercentageInput.value)

    if (chosenPercentageInput.value.length >= 1) {
        if (parsedValue === NaN){
            chosenPercentageInput.value = 0
            currentPercentageNumericValue = 0
        } else {
            chosenPercentageInput.value = parsedValue
            currentPercentageNumericValue = parsedValue
        }
    }
}

function setNotificationValue() {
    if (chosenPercentageInput.value !== "") {
        let stockNotificationValue = currentStockNumericValue + (currentStockNumericValue * currentPercentageNumericValue / 100)
        notificationValue.innerText = "You will get an SMS notification when stock reaches " + stockNotificationValue.toFixed(2) + "$"
    }
}

async function requestGraphForStock(abbreviation){

    const csrftoken  = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const response = await fetch('/getStocksGraph/' + abbreviation +"/",{
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        credentials: 'include',
        mode: 'same-origin'
    })
    return response.json()
}

function addNotification() {
    if (currentStockNumericValue !== 0 && currentPercentageNumericValue !== 0){
        sendNotificationRequest()
            .then(data => {
                if (data.status_code === 200){
                    console.log('success')
                    const numOfNotificationsElement = document.getElementById("numOfNotifications")
                    const numOfNotificationsString = numOfNotificationsElement.innerText
                    let numOfNotifications = Number.parseInt(numOfNotificationsString)
                    numOfNotifications += 1
                    numOfNotificationsElement.innerText = numOfNotifications

                } else {
                    console.log('failure')
                }
            })
            .catch(error => {
                console.log(error)
            })
    }
}

async function sendNotificationRequest(){

    const csrftoken  = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const response = await fetch('/addNotification/',{
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin',
        body: JSON.stringify({
            'name': currentStockName,
            'abbreviation': currentStockAbbreviation,
            'value': currentStockNumericValue,
            'percentage': currentPercentageNumericValue
        })
    })
    return response.json()
}

function animateChartInfo(targetedStock, targetedChartDiv) {

    if (targetedStock.style.paddingBottom === "4%"){
        $(targetedStock).animate({
            paddingBottom: "0.5%",
            width: "100%"
        }, 400, "linear", () => {
            targetedChartDiv.classList.toggle("chart-info-show")

            $(targetedChartDiv).animate({
                opacity: "0.0"
            }, 400)
        })
    } else {
        $(targetedStock).animate({
            paddingBottom: "4%",
            width: "100%"
        }, 400, "linear", () => {
            targetedChartDiv.classList.toggle("chart-info-show")

            $(targetedChartDiv).animate({
                opacity: "1.0"
            }, 400)
        })
    }
}

function addMouseAnimation(element){
    element.addEventListener("mouseover", (event) => {
        event.target.style.opacity = 0.5
    })

    element.addEventListener("mouseout", (event) => {
        event.target.style.opacity = 1.0
    })
}

showNotificationSetup.forEach(element => {
    element.addEventListener("click", toggleModal)

    addMouseAnimation(element)
})

showDropdownElement.forEach(element => {
    element.addEventListener("click", toggleDropdown)

    addMouseAnimation(element)
})

close.addEventListener("click", toggleModal)
window.addEventListener("click", windowOnClick)
chosenPercentageInput.addEventListener("keyup", calculateNotificationValue)
addNotificationButton.addEventListener('click', addNotification)