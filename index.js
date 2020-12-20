"use strct";

const { app, Menu, BrowserWindow } = require("electron");

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
