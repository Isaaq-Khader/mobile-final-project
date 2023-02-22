using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HeadsetRay : MonoBehaviour
{
    public AudioSource meters20;
    public AudioSource meters10;
    public AudioSource meters5;
    public TextMesh distanceText;

    // Start is called before the first frame update
    void Start()
    {
        meters20 = GetComponent<AudioSource>();
        meters20.Stop();
    }

    // Update is called once per frame
    void Update()
    {
        RaycastHit hitInfo;
        if (Physics.Raycast(
                Camera.main.transform.position,
                Camera.main.transform.forward,
                out hitInfo,
                20.0f,
                Physics.DefaultRaycastLayers))
        {
            if (hitInfo.distance < 5)
            {
                distanceText.text = "5m distance: " + hitInfo.distance.ToString();
                
                meters20.Stop();
                meters10.Stop();
                meters5.Play();
            }
            else if (hitInfo.distance > 5 && hitInfo.distance < 10)
            {
                distanceText.text = "10m distance: " + hitInfo.distance.ToString();
                meters20.Stop();
                meters10.Play();
                meters5.Stop();
            }
            else if (hitInfo.distance > 10 && hitInfo.distance < 20)
            {
                distanceText.text = "20m distance: " + hitInfo.distance.ToString();
                meters20.Play();
                meters10.Stop();
                meters5.Stop();
            }
            
        }
    }
}
