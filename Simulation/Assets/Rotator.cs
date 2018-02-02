using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using IronPython.Hosting;
using IronPython.Runtime;
using Microsoft.Scripting.Hosting;
using System;

public class Rotator : MonoBehaviour {
	private ScriptEngine engine;
	private ScriptScope scope;
	private ScriptSource source;

	float time = 100.0f;


	// Use this for initialization
	void Start () {
		engine = Python.CreateEngine ();
		scope = engine.CreateScope ();
		source = engine.CreateScriptSourceFromFile ("PhyEng.py");
	}
	
	// Update is called once per frame
	void Update () {
		source.Execute (scope);

		var getPosition = scope.GetVariable<Func<PythonTuple>> ("getPosition");
		var x = getPosition ();

		float posX = (float)((double)x [0]);
		float posY = (float)((double)x [1]);
		float posZ = (float)((double)x [2]);

		var position = new Vector3 (posX, posY, posZ);

		if (time < 0.0f) {
			transform.localPosition = position;
		} else {
			time -= 1.0f;
		}
	}
}
