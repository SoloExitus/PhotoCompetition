const notificationSocket = new WebSocket(`ws://${window.location.host}/ws/notifications/`);
const likeSocket= new WebSocket(`ws://${window.location.host}/ws/likes/`);

notificationSocket.onmessage = function (e)
{
    let data = e.data;
    //let data = JSON.parse(e.data);
    console.log(data)
}

likeSocket.onmessage = function (e)
{
    let data = JSON.parse(e.data);
    console.log(data)
}