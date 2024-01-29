using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using TMPro;
using System.Globalization;
using UnityEngine.XR.Interaction.Toolkit;

public class CSVExporter : MonoBehaviour
{
    private string filePath;
    private StreamWriter fileWriter;
    private float recordingInterval = 0.5f;
    private float popupInterval = 60f;
    private int isSick = 0;
    private bool playerResponded = false;
    private bool isRecordingEnabled = true;

    public Canvas popupCanvas;
    public TextMeshProUGUI popupText;
    public Button negativeButton;
    public Button neutralButton;
    public Button positiveButton;

    void Start()
    {
        CultureInfo customCulture = (CultureInfo)CultureInfo.CurrentCulture.Clone();
        customCulture.NumberFormat.NumberDecimalSeparator = ".";
        System.Threading.Thread.CurrentThread.CurrentCulture = customCulture;

        string timestamp = System.DateTime.Now.ToString("yyyyMMddHHmmss");
        string dataPath = Application.persistentDataPath;
        filePath = Path.Combine(dataPath, "PlayerData_" + timestamp + ".csv");
        fileWriter = File.CreateText(filePath);
        Debug.Log("CSV file saved to: " + filePath);
        fileWriter.WriteLine("Time, X, Y, Z, Rotation, isSick");

        popupCanvas.gameObject.SetActive(false);
        negativeButton.onClick.AddListener(() => { AnswerButtonClicked(-1); });
        neutralButton.onClick.AddListener(() => { AnswerButtonClicked(0); });
        positiveButton.onClick.AddListener(() => { AnswerButtonClicked(1); });

        StartCoroutine(ShowPopupRoutine());
    }

    void RecordPlayerData()
    {
        if (isRecordingEnabled)
        {
            Vector3 playerPosition = transform.position;
            float playerRotation = transform.rotation.eulerAngles.y;
            float currentTime = Time.time;
            string data = currentTime + "," + playerPosition.x + "," + playerPosition.y + "," + playerPosition.z + "," + playerRotation + "," + isSick;
            fileWriter.WriteLine(data);
        }
    }

    IEnumerator ShowPopupRoutine()
    {
        while (true)
        {
            popupCanvas.gameObject.SetActive(true);
            StopDataRecording();
            popupText.text = "How do you feel?";
            playerResponded = false;
            yield return new WaitUntil(() => playerResponded);
            popupCanvas.gameObject.SetActive(false);
            StartDataRecording();
            yield return new WaitForSeconds(popupInterval);
        }
    }

    void AnswerButtonClicked(int response)
    {
        isSick = response;
        playerResponded = true;
    }

    void StartDataRecording()
    {
        if (isRecordingEnabled)
        {
            InvokeRepeating("RecordPlayerData", 0, recordingInterval);
        }
    }

    void StopDataRecording()
    {
        CancelInvoke("RecordPlayerData");
    }

    void OnDestroy()
    {
        CancelInvoke("RecordPlayerData");
        fileWriter.Close();
    }
}
