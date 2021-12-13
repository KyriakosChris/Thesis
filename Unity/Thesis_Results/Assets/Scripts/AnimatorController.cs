using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimatorController : MonoBehaviour
{
    public Animator anime;
    AnimationClip[] animationClips;
    int count = 0;
    // Start is called before the first frame update
    void Start()
    {
        anime = GetComponent<Animator>();
        animationClips = anime.runtimeAnimatorController.animationClips;
    }

    // Update is called once per frame
    void Update()
    {

        if (ColliderScript.ChangeAnim)
        {
            ColliderScript.ChangeAnim = false;
            anime.Play(animationClips[count].name);
            count++;
            if (animationClips.Length == count)
                count = 0;
        }

    }
}
