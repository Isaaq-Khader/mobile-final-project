using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HeadsetRay : MonoBehaviour
{
    public AudioSource woosh;
    public AudioSource boom;
    public AudioSource bonk;
    public TextMesh distanceText;

    // Start is called before the first frame update
    void Start()
    {
        woosh = GetComponent<AudioSource>();
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
                if (!bonk.isPlaying)
                {
                    boom.Pause();
                    bonk.Play();
                }
            }
            else if (hitInfo.distance >= 5 && hitInfo.distance < 10)
            {
                distanceText.text = "10m distance: " + hitInfo.distance.ToString();
                if (!boom.isPlaying)
                {
                    bonk.Pause();
                    boom.Play();
                    
                }
            }
            else if (hitInfo.distance >= 10 && hitInfo.distance < 20)
            {
                distanceText.text = "20m distance: " + hitInfo.distance.ToString();
                if (!bonk.isPlaying)
                {
                    boom.Pause();
                    bonk.Play();
                }
            }
            else
            {
                distanceText.text = "greater than 20m distance? " + hitInfo.distance.ToString();
            }
            
        }
        else
        {
            distanceText.text = "not close enough";
        }
    }
}
