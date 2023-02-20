using System.Collections.Generic;
using UnityEngine;

public class CoolCollider : MonoBehaviour
{
	public bool useHaptics = true;
	public bool useSound = true;

	public OVRInput.Controller controller;

	private AudioSource cachedSource;
	private OVRHapticsClip hapticsClip;
	private float hapticsClipLength;
	private float hapticsTimeout;

	void OnTriggerEnter(Collider c)
	{
		if (useHaptics)
			PlayHaptics(c);

	}

	void OnCollisionEnter(Collision c)
	{
		if (useHaptics)
			PlayHaptics(c.collider);
		
	}

	void PlayHaptics(Collider c)
	{



		if (controller == OVRInput.Controller.LTouch)
			OVRHaptics.LeftChannel.Preempt(hapticsClip);
		else
			OVRHaptics.RightChannel.Preempt(hapticsClip);
	}

    OVRInput.Controller controller = side == Side.Left ? OVRInput.Controller.LTouch : OVRInput.Controller.RTouch;
    controller.SendHapticImpulse(0.5f, 0.5f, 0.5f);
}
