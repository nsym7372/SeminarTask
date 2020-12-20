"use strct";

const { app, Menu, BrowserWindow } = require("electron");
const path = require("path");

// メインウィンドウはGCされないようにグローバル宣言
let mainWindow = null;

// 全てのウィンドウが閉じたら終了
app.on("window-all-closed", () => {
  if (process.platform != "darwin") {
    app.quit();
  }
});

app.on("will-finish-launching", () => {
  console.log("will-finish-lanching");
});

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1366,
    height: 768,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true,
      // contextIsolation: true,
      //preload: path.join(app.getAppPath(), "preload.js"),
    },
  });

  mainWindow.on("closed", () => {
    win = null;
  });
  mainWindow.webContents.openDevTools();
  mainWindow.loadFile("index.html");
  //mainWindow.loadFile("changeMenu.html");
}

function createMenu() {
  let menu_tmp = [
    {
      label: "File",
      submenu: [
        {
          label: "New",
          click: () => {
            console.log("new clicked");
            createWindow();
          },
        },
        {
          label: "File",
          click: () => {
            console.log("file clicked");
            createWindow();
          },
        },
        { role: "close", lable: "閉じる" },
        { type: "separator" },
        { role: "quit", label: "終了" },
      ],
    },
  ];

  let menu = Menu.buildFromTemplate(menu_tmp);
  Menu.setApplicationMenu(menu);
}

createMenu();
app.whenReady().then(createWindow);

// // Electronの初期化完了後に実行
// app.on("ready", () => {
//   //ウィンドウサイズを1280*720（フレームサイズを含まない）に設定する
//   mainWindow = new BrowserWindow({
//     width: 1280,
//     height: 720,
//     useContentSize: true,
//     webPreferences:{
//       nodeIntegration: true,
//       contextIsolation: true
//     }
//   });

//   //使用するhtmlファイルを指定する
//   mainWindow.loadURL(`file://${__dirname}/index.html`);
//   mainWindow.webContents.openDevTools();

//   // ウィンドウが閉じられたらアプリも終了
//   mainWindow.on("closed", () => {
//     mainWindow = null;
//   });
// });
