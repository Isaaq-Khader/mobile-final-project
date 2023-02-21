using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HeadsetRay : MonoBehaviour
{
    public AudioSource audioData;
    // Start is called before the first frame update
    void Start()
    {
        audioData = GetComponent<AudioSource>();

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
            audioData.PlayOneShot(audioData.clip, 0.5f);
            print(hitInfo.distance);
            
        }
    }
}
