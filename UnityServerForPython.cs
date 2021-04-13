using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class UnityServerForPython : MonoBehaviour 
{
    #region private members 	
    /// <summary> 	
    /// TCPListener to listen for incomming TCP connection 	
    /// requests. 	
    /// </summary> 	
    private TcpListener tcpListener;
    /// <summary> 
    /// Background thread for TcpServer workload. 	
    /// </summary> 	
    private Thread tcpListenerThread;
    /// <summary> 	
    /// Create handle to connected tcp client. 	
    /// </summary> 	
    private TcpClient connectedTcpClient;
    #endregion
    private const int port = 60600;
    private const int buffersize = 1024;
    string clientMessage = "";

    // Use this for initialization
    void Start()
    {

        // Start TcpServer background thread 		
        tcpListenerThread = new Thread(new ThreadStart(ListenForIncommingRequests));
        tcpListenerThread.IsBackground = true;
        tcpListenerThread.Start();
    }

    // Update is called once per frame
    void Update()
    {
        if (clientMessage != "") //functions cannot be called in a Thread, so this thing here exists
        {
            string message = clientMessage;
            clientMessage = "";
            //ActionDecoder.instance.MessageDecoder(message); Call any other script here
        }

    }

    /// <summary> 	
    /// Runs in background TcpServerThread; Handles incomming TcpClient requests 	
    /// </summary> 	
    private void ListenForIncommingRequests()
    {
        try
        {
            // Create listener on localhost port 60600. 			
            tcpListener = new TcpListener(IPAddress.Parse("127.0.0.1"), port);
            tcpListener = new TcpListener(IPAddress.Parse("0.0.0.0"), port); // use 0.0.0.0 when client runs on other machine
            tcpListener.Start();
            Debug.Log("Server is listening");
            Byte[] bytes = new Byte[buffersize];
            while (true)
            {
                using (connectedTcpClient = tcpListener.AcceptTcpClient())
                {
                    // Get a stream object for reading 					
                    using (NetworkStream stream = connectedTcpClient.GetStream())
                    {
                        int length;
                        // Read incomming stream into byte arrary. 						
                        while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
                        {
                            var incommingData = new byte[length];
                            Array.Copy(bytes, 0, incommingData, 0, length);
                            // Convert byte array to string message. 							
                            clientMessage = Encoding.UTF8.GetString(incommingData);
                            //Debug.Log("client message received as: " + clientMessage);

                            //get the actual message
                            if (clientMessage != "[]")
                            {
                                string[] split = new string[] { '"' + "text" + '"' + ":" + '"' };
                                if (clientMessage.Split(split, StringSplitOptions.None).Length > 1)
                                    clientMessage = clientMessage.Split(split, StringSplitOptions.None)[1];
                                clientMessage = clientMessage.Split('"')[0];
                            }
                            else
                            {
                                print("recieved empty client message");
                                clientMessage = "";
                            }

                        }
                    }
                }
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("SocketException " + socketException.ToString());
        }
    }
}