using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace PoseEstimationUI
{
    using System.IO;
    using Microsoft.Win32;
    using System.Diagnostics;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void FileOpenButton_Click(object sender, RoutedEventArgs e)
        {
            var dialog = new OpenFileDialog();
            dialog.Title = "ファイルを開く";
            dialog.Filter = "全てのファイル(*.*)|*.*";
            if (dialog.ShowDialog() == true)
            {
                this.TxFIle.Text = Path.GetFileName(dialog.FileName);
            }
        }

        private void PythonCall(string program, string args = "")
        {
            ProcessStartInfo psInfo = new ProcessStartInfo();

            // コマンド
            psInfo.FileName = "Python";
            psInfo.Arguments = (args == "") ? "" : string.Format("{0} {1}", program, args);

            // コンソール・ウィンドウを開かない、シェル機能を使用しない
            psInfo.CreateNoWindow = true;

            psInfo.UseShellExecute = false;

            // 標準出力をリダイレクトする
            psInfo.RedirectStandardOutput = true;

            // プロセスを開始
            Process p = Process.Start(psInfo);
            

            //// アプリのコンソール出力結果を全て受け取る
            //string line;
            //while ((line = p.StandardOutput.ReadLine()) != null)
            //{
            //    yield return line + Environment.NewLine;
            //}
        }
    }
}
