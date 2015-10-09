///audio_play_footsteps(emitter,loops,priority,audio1,audio2,...);

var i, random_pick, random_argument, sound_file, audioX, audioY;

for (i=3; i< 10; i++)
{
    if (argument_count > i)
    {
       random_argument[i] = argument[i]
    }
    else
    {
       random_argument[i] = -1;
    }
}

random_pick = irandom_range(3,(argument_count-1));
sound_file = random_argument[random_pick];

audioX = controller_camera.x - argument[0];
audioY = controller_camera.y - argument[1];

var playSound = true;
for (var j=3; j<argument_count; j++)
{
    if audio_is_playing(argument[j]) playSound = false;
}
if (playSound) audio_play_sound_on(argument[0],sound_file,argument[1],argument[2]);