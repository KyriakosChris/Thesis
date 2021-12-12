using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Collider : MonoBehaviour
{
    void onCollisionEnter(Collision col){

        Debug.Log(col.collider.name);

    }
}
