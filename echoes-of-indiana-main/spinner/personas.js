/**
 * ECHOES OF INDIANA — PERSONA DATA FOR SPINNER
 * 
 * Categories:
 * - archetypes: Composite characters representing Indiana workers/eras
 * - historical: Real historical figures from Indiana
 * - living: Still-living Indiana legends
 * - lore: Mythical, cryptid, or supernatural figures
 * 
 * Status:
 * - active: Has Simli agentId + faceId, ready to use
 * - placeholder: Planned, needs Simli setup
 */

export const CATEGORIES = {
  archetypes: { id: 'archetypes', name: 'Composite Archetypes', color: '#7c3aed' },
  historical: { id: 'historical', name: 'Historical Figures', color: '#0891b2' },
  living: { id: 'living', name: 'Living Legends', color: '#059669' },
  lore: { id: 'lore', name: 'Local Lore', color: '#dc2626' },
};

export const PERSONAS = [
  // ═══════════════════════════════════════════
  // COMPOSITE ARCHETYPES
  // ═══════════════════════════════════════════
  {
    id: 'mabel',
    name: 'Mabel',
    category: 'archetypes',
    title: 'Showers Finishing Worker, 1917',
    quote: 'I sand till the grain lies flat.',
    status: 'active',
    agentId: '2c8b6f6d-cb83-4100-a99b-ee33f808069a',
    faceId: '33622e5c-6107-4da0-9794-8ea784ccdb43',
    menuVideo: 'Mabel_Menu.mp4',
  },
  {
    id: 'tomaz',
    name: 'Tomaz',
    category: 'archetypes',
    title: 'Limestone Channeler, 1923',
    quote: 'Cold bar, warm stone.',
    status: 'active',
    agentId: 'b25bed51-b7a9-4fa7-b3e4-1c646c5740a2',
    faceId: 'd8a37d32-1eae-45de-8085-1c510773cf52',
    menuVideo: 'Tomaz_Menu.mp4',
  },
  {
    id: 'hazel',
    name: 'Hazel',
    category: 'archetypes',
    title: 'RCA Quality Control Inspector, 1958',
    quote: 'Check the solder, check the tube.',
    status: 'active',
    agentId: '2e04edd9-a863-4cf3-a425-e2fcd9307f12',
    faceId: 'f4db617d-94f8-4e55-80fe-a16507da2505',
    menuVideo: 'Hazel_Menu.mp4',
  },
  {
    id: 'nell',
    name: 'Nell',
    category: 'archetypes',
    title: 'Telephone Operator, 1942',
    quote: 'Number please.',
    status: 'placeholder',
  },
  {
    id: 'mae',
    name: 'Mae',
    category: 'archetypes',
    title: 'Ball Jar Canner, 1910',
    quote: 'Seal it tight or lose the summer.',
    status: 'placeholder',
  },
  {
    id: 'cyril',
    name: 'Cyril',
    category: 'archetypes',
    title: 'Interurban Motorman, 1925',
    quote: 'All aboard for Indianapolis.',
    status: 'placeholder',
  },
  {
    id: 'eddie',
    name: 'Eddie',
    category: 'archetypes',
    title: 'Auto Worker, 1955',
    quote: 'Assembly never stops.',
    status: 'placeholder',
  },
  {
    id: 'ccc-worker',
    name: 'CCC Worker',
    category: 'archetypes',
    title: 'Civilian Conservation Corps, 1935',
    quote: 'We built these trails with our hands.',
    status: 'placeholder',
  },

  // ═══════════════════════════════════════════
  // HISTORICAL FIGURES
  // ═══════════════════════════════════════════
  {
    id: 'riley',
    name: 'James Whitcomb Riley',
    category: 'historical',
    title: 'The Hoosier Poet, 1849-1916',
    quote: 'The ripest peach is highest on the tree.',
    status: 'active',
    agentId: '9a22d997-e5b7-4388-bd45-2135fc75c20a',
    faceId: 'b52e6173-4a03-49a5-81ed-409f9fbb9d08',
    menuVideo: 'James_Whitcomb_Riley_Menu.mp4',
  },
  {
    id: 'vonnegut',
    name: 'Kurt Vonnegut',
    category: 'historical',
    title: 'Indianapolis Author, 1922-2007',
    quote: 'So it goes.',
    status: 'placeholder',
  },
  {
    id: 'wells',
    name: 'Herman B Wells',
    category: 'historical',
    title: 'IU President, 1902-2000',
    quote: 'The purpose of education is to develop the mind.',
    status: 'placeholder',
  },
  {
    id: 'walker',
    name: 'Madam C.J. Walker',
    category: 'historical',
    title: 'Entrepreneur, 1867-1919',
    quote: 'I got my start by giving myself a start.',
    status: 'placeholder',
  },
  {
    id: 'dean',
    name: 'James Dean',
    category: 'historical',
    title: 'Rebel from Fairmount, 1931-1955',
    quote: 'Dream as if you\'ll live forever.',
    status: 'placeholder',
  },
  {
    id: 'carmichael',
    name: 'Hoagy Carmichael',
    category: 'historical',
    title: 'Composer from Bloomington, 1899-1981',
    quote: 'Stardust memories.',
    status: 'placeholder',
  },
  {
    id: 'kinsey',
    name: 'Alfred Kinsey',
    category: 'historical',
    title: 'Researcher, 1894-1956',
    quote: 'The only unnatural sex act is that which you cannot perform.',
    status: 'placeholder',
  },
  {
    id: 'lombard',
    name: 'Carole Lombard',
    category: 'historical',
    title: 'Fort Wayne Actress, 1908-1942',
    quote: 'I live by a man\'s code.',
    status: 'placeholder',
  },
  {
    id: 'pyle',
    name: 'Ernie Pyle',
    category: 'historical',
    title: 'War Correspondent, 1900-1945',
    quote: 'I write from the worm\'s eye view.',
    status: 'placeholder',
  },
  {
    id: 'charleston',
    name: 'Oscar Charleston',
    category: 'historical',
    title: 'Baseball Legend, 1896-1954',
    quote: 'Play the game.',
    status: 'placeholder',
  },
  {
    id: 'montgomery',
    name: 'Wes Montgomery',
    category: 'historical',
    title: 'Jazz Guitarist, 1923-1968',
    quote: 'I never practice my guitar.',
    status: 'placeholder',
  },
  {
    id: 'ostrom',
    name: 'Elinor Ostrom',
    category: 'historical',
    title: 'Nobel Economist, 1933-2012',
    quote: 'People can govern the commons.',
    status: 'placeholder',
  },
  {
    id: 'white',
    name: 'Ryan White',
    category: 'historical',
    title: 'AIDS Activist, 1971-1990',
    quote: 'I came face to face with death.',
    status: 'placeholder',
  },

  // ═══════════════════════════════════════════
  // LIVING LEGENDS
  // ═══════════════════════════════════════════
  {
    id: 'bird',
    name: 'Larry Bird',
    category: 'living',
    title: 'The Hick from French Lick, 1956-',
    quote: 'Give 100% all of the time.',
    status: 'placeholder',
  },
  {
    id: 'mellencamp',
    name: 'John Mellencamp',
    category: 'living',
    title: 'Rock Icon from Seymour, 1951-',
    quote: 'I was born in a small town.',
    status: 'placeholder',
  },
  {
    id: 'letterman',
    name: 'David Letterman',
    category: 'living',
    title: 'Late Night Host, 1947-',
    quote: 'Home office: Wahoo, Nebraska.',
    status: 'placeholder',
  },
  {
    id: 'carter',
    name: 'Vivian Carter',
    category: 'living',
    title: 'Vee-Jay Records Founder, 1921-1989',
    quote: 'The music speaks.',
    status: 'placeholder',
  },
  {
    id: 'brown',
    name: 'Angela Brown',
    category: 'living',
    title: 'Opera Singer, 1964-',
    quote: 'Indiana trained my voice.',
    status: 'placeholder',
  },

  // ═══════════════════════════════════════════
  // LOCAL LORE
  // ═══════════════════════════════════════════
  {
    id: 'bigfoot',
    name: 'Brown County Bigfoot',
    category: 'lore',
    title: 'Trail Sage & Cryptid Teller',
    quote: 'Need miles, water, or a creature tale?',
    status: 'active',
    agentId: '4a11ab79-d20e-4277-8e94-82252e723b4d',
    faceId: 'cd6ce7ae-9317-4478-a889-a32877b176ca',
    menuVideo: 'Bigfoot_Menu_Better.mp4',
  },
  {
    id: 'oracle',
    name: 'Hoosier Oracle',
    category: 'lore',
    title: 'Echoes Guide',
    quote: 'Ask your question; I will route you.',
    status: 'placeholder',
  },
  {
    id: 'ghostlight',
    name: 'Moody\'s Light',
    category: 'lore',
    title: 'Phantom of Francesville',
    quote: 'Some say it\'s swamp gas. I know better.',
    status: 'placeholder',
  },
  {
    id: 'lilbub',
    name: 'Lil Bub',
    category: 'lore',
    title: 'Bloomington\'s Cosmic Cat, 2011-2019',
    quote: 'Good job, bub.',
    status: 'placeholder',
  },
];

// Utility functions
export function getPersonasByCategory(categoryId) {
  if (categoryId === 'all') return PERSONAS;
  return PERSONAS.filter(p => p.category === categoryId);
}

export function getActivePersonas() {
  return PERSONAS.filter(p => p.status === 'active');
}

export function shuffleArray(arr) {
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}


