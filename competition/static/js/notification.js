const notificationSocket = new WebSocket('ws://localhost:8000/ws/notifications/');

notificationSocket.onmessage = function (e)
{
    let data = e.data;
    //let data = JSON.parse(e.data);
    console.log(data)
}