using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using TMPro;
using System.Globalization;

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
        negativeButton.onClick.AddListener(NegativeButtonClicked);
        neutralButton.onClick.AddListener(NeutralButtonClicked);
        positiveButton.onClick.AddListener(PositiveButtonClicked);

        StartCoroutine(ShowPopupRoutine());
        StartDataRecording();
    }

    void RecordPlayerData()
    {
        if (isRecordingEnabled)
        {
            Vector3 playerPosition = transform.position;
            Quaternion playerRotation = transform.rotation;
            float currentTime = Time.time;
            string data = string.Format("{0},{1},{2},{3},{4},{5}", currentTime, playerPosition.x, playerPosition.y, playerPosition.z, playerRotation.eulerAngles.y, isSick);
            fileWriter.WriteLine(data);
        }
    }

    IEnumerator ShowPopupRoutine()
    {
        while (true)
        {
            popupCanvas.gameObject.SetActive(true);
            isRecordingEnabled = false; // Suspendre l'enregistrement des données pendant que la popup est affichée
            popupText.text = "How do you feel?";
            playerResponded = false;
            yield return new WaitUntil(() => playerResponded);
            popupCanvas.gameObject.SetActive(false);
            isRecordingEnabled = true; // Reprendre l'enregistrement des données
            yield return new WaitForSeconds(popupInterval);
        }
    }

    void NegativeButtonClicked()
    {
        isSick = -1;
        playerResponded = true;
    }

    void NeutralButtonClicked()
    {
        isSick = 0;
        playerResponded = true;
    }

    void PositiveButtonClicked()
    {
        isSick = 1;
        playerResponded = true;
    }

    void StartDataRecording()
    {
        InvokeRepeating("RecordPlayerData", 0, recordingInterval);
    }

    void OnDestroy()
    {
        CancelInvoke("RecordPlayerData");
        fileWriter.Close();
    }
}
