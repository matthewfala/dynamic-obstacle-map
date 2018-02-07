using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace AssemblyCSharp
{
public class Cubemind : MonoBehaviour {

	// Use this for initialization
	public State state;
	void Start () {

	}
	public void newState(State s)
	{
			state = s;
			Transform target;

			Vector3 v = Vector3.zero;
			transform.position = Vector3.SmoothDamp(transform.position, new Vector3(s.x,s.y,s.z), ref v,0.3F);
			print("trans");
	}
	// Update is called once per frame
	void Update () {
		
	}
}
}
