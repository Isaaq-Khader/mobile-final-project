using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HeadsetRay : MonoBehaviour
{
    public AudioSource meters20;
    public AudioSource meters10;
    public AudioSource meters5;
    // Start is called before the first frame update
    void Start()
    {
        meters20 = GetComponent<AudioSource>();
        meters10 = GetComponent<AudioSource>();
        meters5 = GetComponent<AudioSource>();

    }

    // Update is called once per frame
    void Update()
    {
        RaycastHit hitInfo;
        if (Physics.Raycast(
                Camera.main.transform.position,
                Camera.main.transform.forward,
                out hitInfo,
                5.0f,
                Physics.DefaultRaycastLayers))
        {
            meters5.Play();
            print(hitInfo.distance);
            
        }
        if (Physics.Raycast(
                Camera.main.transform.position,
                Camera.main.transform.forward,
                out hitInfo,
                20.0f,
                Physics.DefaultRaycastLayers))
        {
            meters20.Play();
            print(hitInfo.distance);
            
        }
        if (Physics.Raycast(
                Camera.main.transform.position,
                Camera.main.transform.forward,
                out hitInfo,
                10.0f,
                Physics.DefaultRaycastLayers))
        {
            meters10.Play();
            print(hitInfo.distance);
            
        }
    }
}
