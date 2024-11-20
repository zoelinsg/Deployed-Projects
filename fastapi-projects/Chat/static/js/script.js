let $ = jQuery;
let socket;

// 初始化 WebSocket 連線
function initializeWebSocket() {
  // 與伺服器建立 WebSocket 連線，連線到 ws://localhost:8000/message
  socket = new WebSocket('ws://localhost:8000/message');

  // 當 WebSocket 連線建立成功時觸發
  socket.onopen = function (event) {
    console.log('WebSocket connection established.');
  };

  // 當從伺服器接收到訊息時觸發
  socket.onmessage = function (event) {
    const data = JSON.parse(event.data); // 將收到的訊息解析成 JSON 格式
    const msgClass = data.isMe ? 'user-message' : 'other-message'; // 根據是否是自己發送的訊息來設定樣式
    const sender = data.isMe ? 'You' : data.username; // 如果是自己發送的訊息，顯示 "You"，否則顯示對方的使用者名稱
    const message = data.data; // 訊息的內容

    // 建立訊息的 HTML 元素
    const messageElement = $('<li>').addClass('clearfix');
    messageElement.append($('<div>').addClass(msgClass).text(sender + ': ' + message));

    // 將訊息元素加入到訊息列表中
    $('#messages').append(messageElement);

    // 自動捲動聊天視窗到底部，確保最新訊息可見
    $('#chat').scrollTop($('#chat')[0].scrollHeight);
  };

  // 當 WebSocket 發生錯誤時觸發
  socket.onerror = function (event) {
    console.error('WebSocket error. Please rejoin the chat.');
    showJoinModal(); // 顯示加入聊天的彈窗
  };

  // 當 WebSocket 關閉時觸發
  socket.onclose = function (event) {
    if (event.code === 1000) {
      // 如果正常關閉，顯示正常關閉訊息
      console.log('WebSocket closed normally.');
    } else {
      // 如果有錯誤代碼，顯示錯誤訊息並要求重新加入
      console.error('WebSocket closed with error code: ' + event.code + '. Please rejoin the chat.');
      showJoinModal(); // 顯示加入聊天的彈窗
    }
  };
}

// 顯示加入聊天的彈窗
function showJoinModal() {
  $('#username-form').show(); // 顯示使用者名稱表單
  $('#chat').hide(); // 隱藏聊天窗口
  $('#message-input').hide(); // 隱藏訊息輸入框
  $('#usernameModal').modal('show'); // 顯示模態框
}

// 點擊「打開彈窗」按鈕時，顯示加入彈窗
$('#open-modal').click(function () {
  showJoinModal();
});

// 當成功加入聊天時，隱藏加入彈窗並顯示聊天介面
function joinChat() {
  $('#username-form').hide(); // 隱藏使用者名稱表單
  $('#chat').show(); // 顯示聊天窗口
  $('#message-input').show(); // 顯示訊息輸入框
  $('#usernameModal').modal('hide'); // 隱藏模態框
}

// 點擊「加入」按鈕時，建立 WebSocket 連線並進入聊天
$('#join').click(function () {
  initializeWebSocket(); // 初始化 WebSocket 連線
  joinChat(); // 切換到聊天視窗
});

// 點擊「發送」按鈕時，發送訊息
$('#send').click(function () {
  sendMessage();
});

// 當按下 Enter 鍵時，發送訊息
$('#message').keydown(function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

// 發送訊息的函數
function sendMessage() {
  const message = $('#message').val(); // 獲取輸入框中的訊息
  if (message) {
    // 使用 WebSocket 將訊息發送到伺服器，並附上使用者名稱
    socket.send(JSON.stringify({ "message": message, "username": $('#usernameInput').val() }));
    $('#message').val(''); // 清空輸入框
  }
}
