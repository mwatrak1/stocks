const stock_items = []
const stock_list = document.querySelectorAll(".stock-item")

window.onload = () => {

    var deleteButton

    for (stock of stock_list){
        console.log(stock)
        var deleteButton = stock.getElementsByClassName("delete-notification")[0]
        deleteButton.addEventListener("click", deleteNotification)
    }
}

const deleteNotification = (element) => {
    var targetId = element.target.parentElement.parentElement.parentElement.id

    sendDeleteNotificationRequest(targetId)
     .then(response => {
         console.log(response)
         const deletedNotification = document.getElementById(targetId)
         deletedNotification.remove()

         const numOfNotificationsElement = document.getElementById("numOfNotifications")
         const numOfNotificationsString = numOfNotificationsElement.innerText
         let numOfNotifications = Number.parseInt(numOfNotificationsString)
         numOfNotifications -= 1
         numOfNotificationsElement.innerText = numOfNotifications
     })
     .catch(err => {
         console.log(err)
     })
    

}

async function sendDeleteNotificationRequest(setup_date){

    const csrftoken  = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const response = await fetch('/deleteNotification/',{
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        credentials: 'include',
        mode: 'same-origin',
        body: JSON.stringify({
            "setup_date": setup_date
        })
    })
    return response.json()
}