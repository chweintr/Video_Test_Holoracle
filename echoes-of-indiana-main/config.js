/**
 * ECHOES OF INDIANA - CONFIGURATION
 * 
 * 4-Layer Compositor Configuration:
 * ┌─────────────────────────────────────────┐
 * │  Layer 4: TOP FLOATIES                  │
 * │  Layer 3: SIMLI AGENT                   │
 * │  Layer 2: ABSTRACT LOOPS / TRANSITIONS  │
 * │  Layer 1: BOTTOM FLOATIES               │
 * └─────────────────────────────────────────┘
 */

const CONFIG = {
    // Backend API endpoint
    backendUrl: window.location.origin,
    tokenEndpoint: '/simli-token',

    /* ============================================
       GLOBAL VIDEO SETTINGS
       These affect multiple personas or global layers
       ============================================ */
    video: {
        // LAYER 1: Bottom Floaties (perpetual loop)
        // Smoke, embers, subtle depth effects behind everything
        bottomFloaties: null, // e.g., 'floaties-bottom.mp4'
        
        // LAYER 4: Top Floaties (perpetual loop)
        // Sparkles, particles, neon wisps on top of everything
        topFloaties: null, // e.g., 'floaties-top.mp4'
        
        // LAYER 2: Idle Loops (random abstract videos)
        // These play when no persona is active
        // The compositor picks randomly from this array
        idleLoops: [
            'idle_1.mp4',
            // Add more idle loops here as you create them:
            // 'idle_2.mp4',
            // 'idle_3.mp4',
        ],
        
        // Randomize idle loop selection (true) or play sequentially (false)
        randomizeIdleLoops: true,
        
        // Default transition duration (ms) - used when no video is configured
        defaultTransitionDuration: 2000,
        
        // Allow user to skip transition by clicking
        allowSkipTransition: false,
        
        // Transition video playback speed (1.0 = normal, 1.5 = 50% faster, 2.0 = double speed)
        // Increase this if your transition video is too long
        transitionPlaybackRate: 1.5,  // ← ADJUST THIS (1.0-2.0)
    },

    /* ============================================
       PERSONAS CONFIGURATION
       Each persona has their own Simli agent, videos, and settings
       ============================================ */
    personas: {
        mabel: {
            name: 'Mabel',
            fullTitle: 'Showers Finishing Worker, 1917',
            quote: '"I sand till the grain lies flat; the whistle tells you what the clock would."',
            description: 'Sanded drawer fronts; helped at the veneer press; counted pieces at the bell during the war years.',

            // Simli Configuration
            agentId: '2c8b6f6d-cb83-4100-a99b-ee33f808069a', // Mabel's Simli Agent ID
            faceId: '33622e5c-6107-4da0-9794-8ea784ccdb43',  // Mabel's Face ID

            // Video Assets (paths relative to assets/videos/)
            videos: {
                // REQUIRED: Transition from idle abstract → persona head appearing
                // Can be a single string OR an array for random selection
                // Last frame should show head in position where Simli will appear
                idleToActive: [
                    'idle_to_mabel_2.mp4',
                    // 'idle_to_mabel_1.MOV',  // Uncomment when ready
                ],
                
                // OPTIONAL: Transition from persona → back to abstract
                // If null, will just fade out. Can also be an array for random selection.
                activeToIdle: null, // e.g., 'mabel_to_idle.mp4' or ['mabel_to_idle_1.mp4', 'mabel_to_idle_2.mp4']
            },

            // Processing Messages (shown during AI latency)
            processingMessages: [
                'Mabel is checking the grain...',
                'Mabel is listening to the whistle...',
                'Mabel is counting the pieces...',
                'Mabel is considering your question...',
            ],

            /* 
             * HEAD POSITIONING
             * 
             * Normally you don't need to adjust this because the CSS 
             * head-container handles uniform sizing. But if your video
             * has the head offset from center, you can fine-tune here.
             * 
             * These values are applied to the head-container for this persona.
             */
            headPosition: {
                // Offset from center (use negative values to move left/up)
                offsetX: '0%',
                offsetY: '0%',
                
                // Scale adjustment (1.0 = no change)
                // Use if Simli head needs to be larger/smaller than video head
                scale: 1.0,
            }
        },

        /* ============================================
           FUTURE PERSONAS - Uncomment and configure as needed
           ============================================ */

        /*
        'hoosier-oracle': {
            name: 'Hoosier Oracle',
            fullTitle: 'Echoes Guide',
            quote: '"Ask your question; I will route you to stone, rail, factory, or code."',
            agentId: 'YOUR_ORACLE_AGENT_ID',
            faceId: null,
            videos: {
                idleToActive: 'idle_to_oracle.mp4',
                activeToIdle: 'oracle_to_idle.mp4',
            },
            processingMessages: [
                'Oracle is routing your query...',
                'Oracle is consulting the echoes...',
                'Oracle is gathering wisdom...',
            ],
            headPosition: {
                offsetX: '0%',
                offsetY: '0%',
                scale: 1.0,
            }
        },

        vonnegut: {
            name: 'Kurt Vonnegut',
            fullTitle: 'Indianapolis Author',
            quote: '"I wanted people to respond as I do to the absurdity."',
            agentId: 'YOUR_VONNEGUT_AGENT_ID',
            faceId: null,
            videos: {
                idleToActive: 'idle_to_vonnegut.mp4',
                activeToIdle: null,
            },
            processingMessages: [
                'Kurt is pondering the absurdity...',
                'Kurt is gathering his thoughts...',
                'So it goes...',
            ],
            headPosition: {
                offsetX: '0%',
                offsetY: '0%',
                scale: 1.0,
            }
        },
        */

        // James Whitcomb Riley - ACTIVE
        riley: {
            name: 'James Whitcomb Riley',
            fullTitle: 'The Hoosier Poet, 1849-1916',
            quote: '"The ripest peach is highest on the tree."',
            description: 'Beloved Indiana poet who wrote in Hoosier dialect. Author of "Little Orphant Annie" and "The Raggedy Man."',
            agentId: '9a22d997-e5b7-4388-bd45-2135fc75c20a',
            faceId: 'b52e6173-4a03-49a5-81ed-409f9fbb9d08',
            videos: {
                idleToActive: [
                    'idle_to_riley.mp4',
                    // Add variants here
                ],
                activeToIdle: null,
            },
            processingMessages: [
                'Riley is searching for the right verse...',
                'Riley is recalling a Hoosier tale...',
                'Riley is composing his thoughts...',
                'The poet ponders...',
            ],
            headPosition: {
                offsetX: '0%',
                offsetY: '0%',
                scale: 1.0,
            }
        },

        // PLACEHOLDER - needs Simli agent/face IDs
        /*

        dean: {
            name: 'James Dean',
            fullTitle: 'Rebel from Fairmount, 1931-1955',
            quote: '"Dream as if you\'ll live forever. Live as if you\'ll die today."',
            description: 'Hollywood icon and cultural rebel. Born in Marion, raised in Fairmount, Indiana. Star of Rebel Without a Cause, East of Eden, and Giant.',
            agentId: 'YOUR_DEAN_AGENT_ID',  // ← Get from Simli
            faceId: 'YOUR_DEAN_FACE_ID',    // ← Get from Simli
            videos: {
                idleToActive: [
                    'idle_to_dean.mp4',
                    // Add variants here
                ],
                activeToIdle: null,
            },
            processingMessages: [
                'Dean is lighting a cigarette...',
                'Dean is leaning against the fence...',
                'Dean is remembering Fairmount...',
                'The rebel reflects...',
            ],
            headPosition: {
                offsetX: '0%',
                offsetY: '0%',
                scale: 1.0,
            }
        },

        bird: {
            name: 'Larry Bird',
            fullTitle: 'The Hick from French Lick, 1956-',
            quote: '"I\'ve got a theory that if you give 100% all of the time, somehow things will work out in the end."',
            description: 'NBA legend from French Lick, Indiana. 3x NBA Champion, 3x MVP, 12x All-Star. The greatest Celtic of all time.',
            agentId: 'YOUR_BIRD_AGENT_ID',  // ← Get from Simli
            faceId: 'YOUR_BIRD_FACE_ID',    // ← Get from Simli
            videos: {
                idleToActive: [
                    'idle_to_bird.mp4',
                    // Add variants here
                ],
                activeToIdle: null,
            },
            processingMessages: [
                'Larry is shooting around...',
                'Larry is studying the play...',
                'Larry is remembering French Lick...',
                'The legend considers...',
            ],
            headPosition: {
                offsetX: '0%',
                offsetY: '0%',
                scale: 1.0,
            }
        },

        carmichael: {
            name: 'Hoagy Carmichael',
            fullTitle: 'Composer from Bloomington, 1899-1981',
            quote: '"I know why the caged bird sings."',
            description: 'Bloomington native and composer who wrote jazz standards including "Stardust" and helped define American popular music.',
            agentId: 'YOUR_CARMICHAEL_AGENT_ID',
            faceId: 'YOUR_CARMICHAEL_FACE_ID',
            videos: { idleToActive: ['idle_to_carmichael.mp4'], activeToIdle: null },
            processingMessages: ['Hoagy is tinkling the ivories...', 'Hoagy is humming a melody...', 'The composer muses...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        // ============================================
        // WORKING-CLASS INDIANA PERSONAS
        // ============================================

        nell: {
            name: 'Nell',
            fullTitle: 'Showers Office Tube Runner, 1918',
            quote: '"A hiss and then a thump in the box; paper rides the air faster than boots."',
            description: 'Packed carriers; watched gauges; moved notes between office and works on the pneumatic lines.',
            agentId: 'YOUR_NELL_AGENT_ID',
            faceId: 'YOUR_NELL_FACE_ID',
            videos: { idleToActive: ['idle_to_nell.mp4'], activeToIdle: null },
            processingMessages: ['Nell is checking the pneumatic lines...', 'Nell is reading the gauges...', 'Paper is on its way...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        mae: {
            name: 'Mae',
            fullTitle: 'Monon Depot Clerk, 1918',
            quote: '"Empties in, loads out; chalk the number, pass the hoop, keep the spur clear."',
            description: 'Logged arrivals; copied orders; routed cars on and off the Showers siding from the west-side depot.',
            agentId: 'YOUR_MAE_AGENT_ID',
            faceId: 'YOUR_MAE_FACE_ID',
            videos: { idleToActive: ['idle_to_mae.mp4'], activeToIdle: null },
            processingMessages: ['Mae is logging arrivals...', 'Mae is chalking the numbers...', 'Mae is routing cars...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        tomaz: {
            name: 'Tomaz',
            fullTitle: 'Limestone Channeler, 1920s',
            quote: '"Cold bar, warm stone; the channeler bites, the powder lifts, the derrick takes the load."',
            description: 'Worked steel and powder to free blocks bound for distant buildings; lived with dust, cold mornings, and hoists.',
            agentId: 'YOUR_TOMAZ_AGENT_ID',
            faceId: 'YOUR_TOMAZ_FACE_ID',
            videos: { idleToActive: ['idle_to_tomaz.mp4'], activeToIdle: null },
            processingMessages: ['Tomaz is working the stone...', 'Tomaz is checking the derrick...', 'The channeler bites...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        cyril: {
            name: 'Cyril',
            fullTitle: 'Town Rider, Late 1970s',
            quote: '"Keep cadence on the hills and tip your cap at the old pits; a finish line is one turn away."',
            description: 'Part of the post-Breaking Away cycling culture; knows loops, cinder tracks, and quarry lore.',
            agentId: 'YOUR_CYRIL_AGENT_ID',
            faceId: 'YOUR_CYRIL_FACE_ID',
            videos: { idleToActive: ['idle_to_cyril.mp4'], activeToIdle: null },
            processingMessages: ['Cyril is finding the cadence...', 'Cyril is checking the route...', 'One more turn...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        louise: {
            name: 'Louise',
            fullTitle: 'RCA Color-TV Assembler, 1954',
            quote: '"Snap the tuner, check the glow, tag a pass, send it down; color looks simple when the bench is right."',
            description: 'Worked early color sets on South Rogers; snap the tuner, check the glow, tag a pass.',
            agentId: 'YOUR_LOUISE_AGENT_ID',
            faceId: 'YOUR_LOUISE_FACE_ID',
            videos: { idleToActive: ['idle_to_louise.mp4'], activeToIdle: null },
            processingMessages: ['Louise is checking the glow...', 'Louise is snapping the tuner...', 'Color coming through...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        frank: {
            name: 'Frank',
            fullTitle: 'RCA Shop Steward, Mid 1960s',
            quote: '"We kept the line honest and the room steady; a paycheck is a decision we make together."',
            description: 'Balanced line speed, safety, and pay during tense meetings; kept the room steady.',
            agentId: 'YOUR_FRANK_AGENT_ID',
            faceId: 'YOUR_FRANK_FACE_ID',
            videos: { idleToActive: ['idle_to_frank.mp4'], activeToIdle: null },
            processingMessages: ['Frank is checking the line...', 'Frank is considering the contract...', 'The room stays steady...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        elsie: {
            name: 'Elsie',
            fullTitle: 'Switchyard Hostler, Mid Century',
            quote: '"Night air and a low lantern; you feel the rail hum before you see the headlight."',
            description: 'Cut and spotted cars at night by lantern and voice in the McDoel yard.',
            agentId: 'YOUR_ELSIE_AGENT_ID',
            faceId: 'YOUR_ELSIE_FACE_ID',
            videos: { idleToActive: ['idle_to_elsie.mp4'], activeToIdle: null },
            processingMessages: ['Elsie is listening to the rails...', 'Elsie is spotting cars...', 'The lantern swings...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        mrsjohnson: {
            name: 'Mrs Johnson',
            fullTitle: 'Community Guide, Mid Century',
            quote: '"We made room for one another in churches, clubs, and shops; walk with me and I will show you what stood where."',
            description: 'Connects visitors to sites where neighbors gathered and pushed for change; churches, clubs, shops.',
            agentId: 'YOUR_MRSJOHNSON_AGENT_ID',
            faceId: 'YOUR_MRSJOHNSON_FACE_ID',
            videos: { idleToActive: ['idle_to_mrsjohnson.mp4'], activeToIdle: null },
            processingMessages: ['Mrs Johnson is remembering...', 'Mrs Johnson is pointing the way...', 'Walk with me...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        eddie: {
            name: 'Eddie',
            fullTitle: 'Showers Pond Kid, 1910s',
            quote: '"We skated till the watchman waved us off; that pond kept the factory running and kept us running too."',
            description: 'Grew up in the shadow of the plant and its water works; skated the company pond.',
            agentId: 'YOUR_EDDIE_AGENT_ID',
            faceId: 'YOUR_EDDIE_FACE_ID',
            videos: { idleToActive: ['idle_to_eddie.mp4'], activeToIdle: null },
            processingMessages: ['Eddie is lacing up skates...', 'Eddie is watching for the watchman...', 'The ice holds...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        // ============================================
        // FAMOUS HOOSIERS
        // ============================================

        kinsey: {
            name: 'Alfred Kinsey',
            fullTitle: 'Sexologist and IU Professor',
            quote: '"The only unnatural sex act is that which you cannot perform."',
            description: 'IU professor whose research changed understanding of human sexuality in America.',
            agentId: 'YOUR_KINSEY_AGENT_ID',
            faceId: 'YOUR_KINSEY_FACE_ID',
            videos: { idleToActive: ['idle_to_kinsey.mp4'], activeToIdle: null },
            processingMessages: ['Dr. Kinsey is reviewing the data...', 'The professor considers...', 'Research continues...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        mellencamp: {
            name: 'John Mellencamp',
            fullTitle: 'Seymour Rocker',
            quote: '"I\'m just trying to tell the truth about the American experience."',
            description: 'Seymour rocker who captured small-town American life through heartland rock anthems and social commentary.',
            agentId: 'YOUR_MELLENCAMP_AGENT_ID',
            faceId: 'YOUR_MELLENCAMP_FACE_ID',
            videos: { idleToActive: ['idle_to_mellencamp.mp4'], activeToIdle: null },
            processingMessages: ['John is tuning the guitar...', 'The heartland calls...', 'Small town, big truth...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        carter: {
            name: 'Vivian Carter',
            fullTitle: 'Vee-Jay Records Co-Founder',
            quote: '"Music doesn\'t know color. Good music is good music."',
            description: 'Gary music executive who co-founded Vee-Jay Records, one of the most successful Black-owned record labels in America.',
            agentId: 'YOUR_CARTER_AGENT_ID',
            faceId: 'YOUR_CARTER_FACE_ID',
            videos: { idleToActive: ['idle_to_carter.mp4'], activeToIdle: null },
            processingMessages: ['Vivian is listening to the track...', 'The music plays...', 'Good music is good music...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        brown: {
            name: 'Angela Brown',
            fullTitle: 'Indianapolis Opera Singer',
            quote: '"Every voice has something beautiful to say if we just listen."',
            description: 'Indianapolis opera singer who broke barriers in classical music and brought world-class performance to Indiana stages.',
            agentId: 'YOUR_BROWN_AGENT_ID',
            faceId: 'YOUR_BROWN_FACE_ID',
            videos: { idleToActive: ['idle_to_brown.mp4'], activeToIdle: null },
            processingMessages: ['Angela is warming up...', 'The aria rises...', 'Every voice matters...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        white: {
            name: 'Ryan White',
            fullTitle: 'Kokomo AIDS Activist, 1971-1990',
            quote: '"I came face to face with death at thirteen years old. I was diagnosed with AIDS."',
            description: 'Kokomo teenager whose courageous battle with AIDS discrimination changed national policy and public understanding.',
            agentId: 'YOUR_WHITE_AGENT_ID',
            faceId: 'YOUR_WHITE_FACE_ID',
            videos: { idleToActive: ['idle_to_white.mp4'], activeToIdle: null },
            processingMessages: ['Ryan is remembering...', 'Courage speaks...', 'The fight continues...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        ostrom: {
            name: 'Elinor Ostrom',
            fullTitle: 'Nobel Prize-Winning Economist',
            quote: '"What we have ignored is what citizens can do and the importance of real involvement."',
            description: 'Nobel Prize-winning economist from IU who studied how communities manage shared resources and challenged traditional economic theory.',
            agentId: 'YOUR_OSTROM_AGENT_ID',
            faceId: 'YOUR_OSTROM_FACE_ID',
            videos: { idleToActive: ['idle_to_ostrom.mp4'], activeToIdle: null },
            processingMessages: ['Professor Ostrom is analyzing...', 'The commons endure...', 'Citizens can do...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        walker: {
            name: 'Madam C. J. Walker',
            fullTitle: 'Indianapolis Entrepreneur',
            quote: '"I want to say to every woman present, don\'t sit down and wait for opportunities to come."',
            description: 'Indianapolis entrepreneur who became America\'s first female self-made millionaire through her hair care and cosmetics empire.',
            agentId: 'YOUR_WALKER_AGENT_ID',
            faceId: 'YOUR_WALKER_FACE_ID',
            videos: { idleToActive: ['idle_to_walker.mp4'], activeToIdle: null },
            processingMessages: ['Madam Walker is building...', 'The empire grows...', 'Don\'t wait...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        letterman: {
            name: 'David Letterman',
            fullTitle: 'Indianapolis Late-Night Legend',
            quote: '"There\'s no business like show business, but there are several businesses like accounting."',
            description: 'Indianapolis native who changed late-night television with his irreverent humor and new comedy formats.',
            agentId: 'YOUR_LETTERMAN_AGENT_ID',
            faceId: 'YOUR_LETTERMAN_FACE_ID',
            videos: { idleToActive: ['idle_to_letterman.mp4'], activeToIdle: null },
            processingMessages: ['Dave is checking the cards...', 'The Top Ten list forms...', 'And the number one...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        lilbub: {
            name: 'Lil Bub',
            fullTitle: 'Bloomington\'s Beloved Internet Sensation',
            quote: '"*gentle purr* Every creature has something special to offer the world."',
            description: 'Bloomington\'s beloved internet sensation who brought joy to millions worldwide and raised awareness for special needs pets.',
            agentId: 'YOUR_LILBUB_AGENT_ID',
            faceId: 'YOUR_LILBUB_FACE_ID',
            videos: { idleToActive: ['idle_to_lilbub.mp4'], activeToIdle: null },
            processingMessages: ['*purr*...', 'Bub is considering...', '*happy chirp*...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        montgomery: {
            name: 'Wes Montgomery',
            fullTitle: 'Indianapolis Jazz Guitarist',
            quote: '"I never practice my guitar. From time to time I just open the case and throw in a piece of raw meat."',
            description: 'Indianapolis jazz guitarist whose thumb-picking technique influenced generations of musicians worldwide.',
            agentId: 'YOUR_MONTGOMERY_AGENT_ID',
            faceId: 'YOUR_MONTGOMERY_FACE_ID',
            videos: { idleToActive: ['idle_to_montgomery.mp4'], activeToIdle: null },
            processingMessages: ['Wes is finding the chord...', 'The thumb picks...', 'Jazz flows...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        lombard: {
            name: 'Carole Lombard',
            fullTitle: 'Fort Wayne-Born Actress',
            quote: '"I live by a man\'s code, designed to fit a man\'s world, yet at the same time I never forget that a woman\'s first job is to choose the right shade of lipstick."',
            description: 'Fort Wayne-born actress who became Hollywood\'s highest-paid star and defined the screwball comedy genre.',
            agentId: 'YOUR_LOMBARD_AGENT_ID',
            faceId: 'YOUR_LOMBARD_FACE_ID',
            videos: { idleToActive: ['idle_to_lombard.mp4'], activeToIdle: null },
            processingMessages: ['Carole is checking her marks...', 'The camera rolls...', 'Screwball genius...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },

        clark: {
            name: 'George Rogers Clark',
            fullTitle: 'Revolutionary War Hero',
            quote: '"Great things have been effected by a few men well conducted."',
            description: 'Revolutionary War hero who conquered the Illinois Country for Virginia and secured Indiana\'s future as American territory.',
            agentId: 'YOUR_CLARK_AGENT_ID',
            faceId: 'YOUR_CLARK_FACE_ID',
            videos: { idleToActive: ['idle_to_clark.mp4'], activeToIdle: null },
            processingMessages: ['General Clark is surveying the frontier...', 'The territory awaits...', 'A few men well conducted...'],
            headPosition: { offsetX: '0%', offsetY: '0%', scale: 1.0 }
        },
        */

        bigfoot: {
            name: 'Brown County Bigfoot',
            fullTitle: 'Trail Sage & Cryptid Teller',
            quote: '"Say whether you need miles, water, or a creature tale for the campfire."',
            agentId: '4a11ab79-d20e-4277-8e94-82252e723b4d',
            faceId: 'cd6ce7ae-9317-4478-a889-a32877b176ca',
            videos: {
                // Array = random selection each time Bigfoot is summoned
                idleToActive: [
                    'idle_to_Bigfoot.mp4',
                    'idle_to_bigfoot_2.mp4',
                    'idle_to_Bigfoot_3.mp4',
                ],
                activeToIdle: null,
            },
            processingMessages: [
                'Bigfoot is sniffing the trail...',
                'Bigfoot is consulting the forest...',
                'Bigfoot is gathering a tale...',
            ],
            headPosition: {
                offsetX: '0%',
                offsetY: '0%',
                scale: 1.0,
            }
        },
    },

    /* ============================================
       UI SETTINGS
       ============================================ */
    ui: {
        showDebugPanel: false, // Use ?debug=true in URL to show
        
        // Anti-Cropping Settings for LED Holograms
        stageInset: '0%', // Inset stage from screen edges (e.g., '5%')
        enableBorderMask: false, // Enable vignette border
        borderMaskOpacity: 0.8, // How dark the border mask should be (0-1)
    },

    /* ============================================
       HEAD CONTAINER SETTINGS
       Global settings for the unified head area
       ============================================ */
    head: {
        // These CSS values control the head container size
        // Both transition videos AND Simli render inside this same container
        // Change these to scale all heads uniformly
        
        // Default size (can be overridden in CSS for responsiveness)
        width: '80vmin',
        height: '80vmin',
        maxWidth: '900px',
        maxHeight: '900px',
    },

    /* ============================================
       STATE MACHINE TIMINGS
       ============================================ */
    timing: {
        // How long to wait for transition video to start
        transitionVideoWaitTime: 2000,
        
        // Rotate processing messages every X ms
        processingMessageRotateInterval: 5000,
        
        // Dismiss transition time (if no video)
        dismissTransitionTime: 500,
        
        // Video crossfade duration (ms)
        crossfadeDuration: 500,
    },

    /* ============================================
       AUDIO SETTINGS
       ============================================ */
    audio: {
        enableBackgroundAmbience: false,
        ambienceVolume: 0.3,
    },
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
