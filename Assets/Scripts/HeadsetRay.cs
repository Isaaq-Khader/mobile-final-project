using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HeadsetRay : MonoBehaviour
{
    public AudioSource sonar;
    public TextMesh distanceText;
    bool audioFinished = true;

    IEnumerator HitRayCoroutine()
    {
        RaycastHit hitInfo;
        if (Physics.Raycast(
                Camera.main.transform.position,
                Camera.main.transform.forward,
                out hitInfo,
                20.0f,
                Physics.DefaultRaycastLayers))
        {
            if (hitInfo.distance <= 1)
            {
                distanceText.text = "1m distance: " + hitInfo.distance.ToString();
                if (!sonar.isPlaying)
                {
                    audioFinished = false;
                    sonar.Play();
                    yield return new WaitForSeconds(0.1f);
                    audioFinished = true;
                }
            }
            else if (hitInfo.distance <= 2)
            {
                distanceText.text = "2m distance: " + hitInfo.distance.ToString();
                if (!sonar.isPlaying)
                {
                    audioFinished = false;
                    sonar.Play();
                    yield return new WaitForSeconds(0.25f);
                    audioFinished = true;
                }
            }
            else if (hitInfo.distance < 5 && hitInfo.distance > 2)
            {
                distanceText.text = "5m distance: " + hitInfo.distance.ToString();
                if (!sonar.isPlaying)
                {
                    audioFinished = false;
                    sonar.Play();
                    yield return new WaitForSeconds(0.5f);
                    audioFinished = true;
                }
            }
            else if (hitInfo.distance >= 5 && hitInfo.distance < 10)
            {
                distanceText.text = "10m distance: " + hitInfo.distance.ToString();
                if (!sonar.isPlaying)
                {
                    audioFinished = false;
                    sonar.Play();
                    yield return new WaitForSeconds(1);
                    audioFinished = true;
                }
            }
            else if (hitInfo.distance >= 10 && hitInfo.distance < 20)
            {
                distanceText.text = "20m distance: " + hitInfo.distance.ToString();
                if (!sonar.isPlaying)
                {
                    audioFinished = false;
                    sonar.Play();
                    yield return new WaitForSeconds(2);
                    audioFinished = true;
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

    // Update is called once per frame
    void Update()
    {
        if (audioFinished)
        {
            StartCoroutine(HitRayCoroutine());
        }
    }
}
