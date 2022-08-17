void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord.xy /iResolution.xy;
    
    vec2 q = uv - vec2(0.34, 0.7);

    vec3 col = mix( vec3(1.0, 0.6, (cos(iTime/10.0)/6.0)), vec3(0.3, 0.2, 1.0), sqrt(uv.y) );
    
    float r = 0.2 + .1 * cos( atan(q.y, q.x) * 10.0 + (50.0*(abs(cos(iTime/2.0))/7.0)) * q.x + cos(iTime/3.0));
    
    col *= smoothstep(r, r + 0.04, length(q));
    
    r = 0.015;
    r += 0.002 * cos(120.0 * q.y);
    
    r += exp(-50.0 * uv.y);
    col *= 1.0 - ( 1.0 - smoothstep( r, r + 0.009, abs(q.x - 0.2 * sin(q.y * -3.0)) )) * (1.0 - smoothstep(0.08, 0.1, q.y));
    
    fragColor = vec4(col,1.0);
}

// refs: https://www.shadertoy.com/view/sltyWB