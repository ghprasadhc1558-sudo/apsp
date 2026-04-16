// Battalion data
const battalionData = {
    1: {
        name: '1st Battalion',
        location: 'Vijayawada',
        image: 'images/battalions/1st-battalion.jpg',
        commandant: 'Shri A.K. Sharma',
        commandantImage: 'images/commandants/1st-commandant.jpg',
        history: 'The 1st Battalion APSP was established in 1993 in Vijayawada. It has played a crucial role in maintaining law and order in the capital region. The battalion has participated in various major operations including crowd control during elections, disaster relief operations, and VIP security duties. Over the years, it has earned a reputation for discipline and professionalism.',
        officers: [
            { rank: 'Additional Commandant', name: 'Shri R.K. Verma' },
            { rank: 'Assistant Commandant', name: 'Shri P.S. Reddy' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'K.Ajay Kumar, RI' },
                { office: 'Quarter Master Office', incharge: 'B. Visheswara Rao, RI' },
                { office: 'Motor Transport Office', incharge: 'D.G.V.S.V.Prasad, RI' }
            ],
            'Companies': [
                { company: 'A Company', incharge: 'D.G.V.S.V.Prasad, RI' },
                { company: 'B Company', incharge: 'D.Srinivasa Rao, RSI' },
                { company: 'C Company', incharge: 'D.G.V.S.V.Prasad, RI' }
            ]
        }
    },
    2: {
        name: '2nd Battalion',
        location: 'Kurnool',
        image: 'images/battalions/2nd-bn-kurnool.jpg',
        commandant: 'Smt M.DEEPIKA',
        commandantImage: 'images/commandants/2nd-commandant.jpg',
        designation: 'Commandant',
        history: 'The 2nd Battalion APSP, stationed in Kurnool, was formed to strengthen security in the Rayalaseema region. The battalion has been instrumental in maintaining peace during sensitive periods and has actively participated in anti-naxal operations. It has also contributed significantly to disaster management and community policing initiatives.',
        officers: [
            { rank: 'Additional Commandant', name: 'V.Nagendra Rao' },
            { rank: 'Assistant Commandant', name: 'D.Venkataramana' },
            { rank: 'Assistant Commandant', name: 'P. Ravi Kiran' },
            { rank: 'Assistant Commandant', name: 'V.Keshava Reddy' },
            { rank: 'Assistant Commandant', name: 'S.Sharfuddin' },
            { rank: 'Assistant Commandant', name: 'S.Mahaboob Basha' }
        ],
        companies: {
            'Group Head': [
                { office: 'Quarter Master Office', incharge: 'M.C.Shaikshavali, RI' },
                { office: 'Head Quarters Office', incharge: 'K.Siva Sankar Rao, RI' },
                { office: 'Motor Transport Office', incharge: 'P.Samba Siva Rao, RI' },
                { office: 'Band', incharge: 'J.Otulesu, RSI' },
                { office: 'JA', incharge: 'J.Otulesu, RSI' },
                { office: 'Training', incharge: 'D.Raju, RI' },
                { office: 'Command And Control', incharge: '' },
                { office: 'BATTALION Welfare Office', incharge: 'R.Prabhakar Rao, RI' }
            ],
            'Company Head': [
                { company: 'C Company', incharge: 'L.Srinivasa Reddy, RI' },
                { company: 'K Company', incharge: 'L.Srinivasa Reddy, RI' },
                { company: 'E Company', incharge: 'T.Rama Rao, RI' },
                { company: 'F Company', incharge: 'G.V.Rami Reddy, RI' },
                { company: 'D/SDRF Company', incharge: 'S.Praveen Kumar, RI' },
                { company: 'G Company', incharge: 'M.Surya Rao, RI' },
                { company: 'H Company', incharge: 'S.Ramakotaiah, RI' },
                { company: 'A Company', incharge: 'A.Gunapathi, RI' },
                { company: 'B Company', incharge: 'D.Raju, RI' }
            ]
        }
    },
    3: {
        name: '3rd Battalion',
        location: 'Kakinada',
        image: 'images/battalions/3rd-battalion.jpg',
        commandant: 'Sri M.Nagendra Rao',
        commandantImage: 'images/commandants/3rd-commandant.jpg',
        designation: 'I/C Commandant',
        history: 'The 3rd Battalion APSP at Kakinada was established to secure the coastal belt of East Godavari district. The battalion has been at the forefront of coastal security operations and has provided critical support during natural calamities like cyclones and floods. It works closely with local administration for maintaining law and order.',
        officers: [
            { rank: 'Additional Commandant', name: 'S.Devananda Rao' },
            { rank: 'Assistant Commandant', name: 'B.Chandra Sekararao' },
            { rank: 'Assistant Commandant', name: 'S.Manmadha Rao' },
            { rank: 'Assistant Commandant', name: 'Sri M.Mohana Rao' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'K.Ajay Kumar, RI' },
                { office: 'Quarter Master Office', incharge: 'B. Visheswara Rao, RI' },
                { office: 'Motor Transport Office', incharge: 'D.G.V.S.V.Prasad, RI' },
                { office: 'Band', incharge: 'Shatara SS, ARSI' },
                { office: 'JA', incharge: 'A.Manikanta, RSI' },
                { office: 'Command And Control', incharge: ', Email id' },
                { office: 'BATTALION Welfare Office', incharge: 'K.Ravishankar, RI' }
            ],
            'Company Head': [
                { company: 'C Company', incharge: 'D.G.V.S.V.Prasad, RI' },
                { company: 'D Company', incharge: 'D.Srinivasa Rao, RSI' },
                { company: 'F Company', incharge: 'D.G.V.S.V.Prasad, RI' },
                { company: 'H Company', incharge: 'K.Satyanarayana, RI' },
                { company: 'Training', incharge: 'K.Ajay Kumar, RI' },
                { company: 'E Company', incharge: 'K.Satyanarayana, RI' },
                { company: 'A Company', incharge: 'K.Satyanarayana, RI' },
                { company: 'D Company', incharge: 'K.Babu Rao, RI' },
                { company: 'APSDRF Company', incharge: 'V.Ramu, RI' }
            ]
        }
    },
    4: {
        name: '4th Battalion',
        location: 'Guntur',
        image: 'images/battalions/4th-battalion.jpg',
        commandant: 'Shri M.P. Singh',
        officers: [
            { rank: 'Additional Commandant', name: 'Shri D.K. Sharma' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'P.Kumar, RI' }
            ],
            'Companies': [
                { company: 'A Company', incharge: 'S.Reddy, RI' }
            ]
        }
    },
    5: {
        name: '5th Battalion',
        location: 'Vizianagaram',
        image: 'images/battalions/5th-bn-vizianagaram.jpg',
        commandant: 'Smt. Malika Garg, IPS',
        commandantImage: 'images/commandants/5th-commandant.jpg',
        designation: 'Commandant',
        history: 'The 5th Battalion APSP, based in Vizianagaram, serves the northern coastal districts of Andhra Pradesh. Established to enhance security infrastructure in the region, the battalion has been actively involved in maintaining communal harmony and conducting specialized training programs. It has a distinguished record in handling law and order situations.',
        officers: [
            { rank: 'Additional Commandant', name: 'M.Venkateswara Rao' },
            { rank: 'Assistant Commandant', name: 'D.V.Ramana Murthy' },
            { rank: 'Assistant Commandant', name: 'G.V.Prabhakar Rao' },
            { rank: 'Assistant Commandant', name: 'S.Bapujee' },
            { rank: 'Assistant Commandant', name: 'K.Sarath Babu' },
            { rank: 'Assistant Commandant', name: 'G.Laxmi Narayana' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'G.Ravindra Kumar, RI' },
                { office: 'Quarter Master Office', incharge: 'V.V.Kesava Ramu, RI' },
                { office: 'Motor Transport Office', incharge: 'A.Srinivasa Rao, RI' },
                { office: 'Training', incharge: 'M.Srinu, RI' },
                { office: 'Band', incharge: 'G.Krishana Rao, ARSI' },
                { office: 'JA', incharge: 'M.Manohara Rao, RSI' },
                { office: 'Command And Control', incharge: '' },
                { office: 'BATTALION Welfare Office', incharge: 'N.Ganesh, RI' }
            ],
            'Company Head': [
                { company: 'A Company', incharge: 'P.Sudhakara Babu, RI' },
                { company: 'G Company', incharge: 'M.Nooka Raju, RI' },
                { company: 'C Company', incharge: 'K.K.M.Raju, RI' },
                { company: 'E Company', incharge: 'S.Raju, RI' },
                { company: 'B Company', incharge: 'K.Samarpana Rao, RI' },
                { company: 'D Company', incharge: 'U.Danayya, RI' },
                { company: 'F Company', incharge: 'G.Damodara Rao, RI' },
                { company: 'H Company/SDRF', incharge: 'S.Chandra Sekhar, RI' }
            ]
        }
    },
    6: {
        name: '6th Battalion',
        location: 'Mangalagiri',
        image: 'images/battalions/6th-bn-mangalagiri.jpg',
        commandant: 'K.Nagesh Babu',
        commandantImage: 'images/commandants/6th-commandant.jpg',
        designation: 'Commandant',
        history: 'The 6th Battalion APSP at Mangalagiri plays a strategic role in providing security to the capital region. Located near Vijayawada-Guntur twin cities, the battalion is frequently deployed for VIP security, election duties, and maintaining public order during major events. It has earned recognition for its operational excellence and dedication to duty.',
        officers: [
            { rank: 'Additional Commandant', name: 'D.Aseervadam' },
            { rank: 'Assistant Commandant', name: 'P.V.Hanumanthu' },
            { rank: 'Assistant Commandant', name: 'Sri U.Ravi' },
            { rank: 'Assistant Commandant', name: 'K.Venkateswara Rao' },
            { rank: 'Assistant Commandant', name: 'D.Venkateswara Rao' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'M.Venkata Rao, RI' },
                { office: 'Quarter Master Office', incharge: 'S.Srinivasa Rao, RI' },
                { office: 'Motor Transport Office', incharge: 'B.Venkata Rao, RI' },
                { office: 'Training', incharge: 'A.Simhadri Naidu, RI' },
                { office: 'Band', incharge: 'S.Srinivasulu, ARSI' },
                { office: 'JA', incharge: 'P.Ibrahim Khan, RSI' },
                { office: 'Command And Control', incharge: '' },
                { office: 'BATTALION Welfare Office', incharge: 'G.Suresh, RI' }
            ],
            'Company Head': [
                { company: 'A Company', incharge: 'K.Yesu Dasu, RI' },
                { company: 'C Company', incharge: 'B. Ramulu, RI' },
                { company: 'E Company', incharge: 'Y.Venkateswarlu, RI' },
                { company: 'D Company', incharge: 'H.Rajasekharam, RI' },
                { company: 'H Company', incharge: 'A.Saleesh, RI' },
                { company: 'K Company', incharge: 'M.Guru Naidu, RI' },
                { company: 'B Company', incharge: 'V.L.Chndra Sekhar, RI' },
                { company: 'G Company', incharge: 'K.P.Das, RI' },
                { company: 'F Company/SDRF', incharge: 'K.Venkateswarlu, RI' }
            ]
        }
    },
    7: {
        name: '7th Battalion',
        location: 'Anantapur',
        image: 'images/battalions/7th-battalion.jpg',
        commandant: 'Shri K.N. Prasad',
        officers: [
            { rank: 'Additional Commandant', name: 'Shri T.R. Singh' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'S.Kumar, RI' }
            ],
            'Companies': [
                { company: 'A Company', incharge: 'P.Reddy, RI' }
            ]
        }
    },
    8: {
        name: '8th Battalion',
        location: 'Kurnool',
        image: 'images/battalions/8th-battalion.jpg',
        commandant: 'Shri B.S. Chauhan',
        officers: [
            { rank: 'Additional Commandant', name: 'Shri M.K. Verma' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'K.Prasad, RI' }
            ],
            'Companies': [
                { company: 'A Company', incharge: 'R.Kumar, RI' }
            ]
        }
    },
    9: {
        name: '9th Battalion',
        location: 'Eluru',
        image: 'images/battalions/9th-battalion.jpg',
        commandant: 'Shri P.V. Rao',
        officers: [
            { rank: 'Additional Commandant', name: 'Shri S.K. Reddy' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'M.Kumar, RI' }
            ],
            'Companies': [
                { company: 'A Company', incharge: 'N.Prasad, RI' }
            ]
        }
    },
    11: {
        name: '11th Battalion',
        location: 'Rajahmundry',
        image: 'images/battalions/11th-battalion.jpg',
        commandant: 'Shri T.R. Krishna',
        officers: [
            { rank: 'Additional Commandant', name: 'Shri V.S. Kumar' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'P.Kumar, RI' }
            ],
            'Companies': [
                { company: 'A Company', incharge: 'S.Reddy, RI' }
            ]
        }
    },
    14: {
        name: '14th Battalion',
        location: 'Kakinada',
        image: 'images/battalions/14th-battalion.jpg',
        commandant: 'Shri N.S. Murthy',
        officers: [
            { rank: 'Additional Commandant', name: 'Shri K.R. Prasad' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'R.Kumar, RI' }
            ],
            'Companies': [
                { company: 'A Company', incharge: 'V.Prasad, RI' }
            ]
        }
    },
    16: {
        name: '16th Battalion',
        location: 'Srikakulam',
        image: 'images/battalions/16th-battalion.jpg',
        commandant: 'Shri G.V. Naidu',
        officers: [
            { rank: 'Additional Commandant', name: 'Shri M.S. Rao' }
        ],
        companies: {
            'Group Head': [
                { office: 'Head Quarters Office', incharge: 'S.Kumar, RI' }
            ],
            'Companies': [
                { company: 'A Company', incharge: 'P.Reddy, RI' }
            ]
        }
    }
};

// Get battalion ID from URL
function getBattalionId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Load battalion details
function loadBattalionDetails() {
    const battalionId = getBattalionId();
    const battalion = battalionData[battalionId];

    if (!battalion) {
        document.getElementById('battalion-title').innerHTML = '<i class="fas fa-exclamation-triangle"></i> Battalion Not Found';
        document.getElementById('battalion-subtitle').textContent = 'Please select a valid battalion';
        return;
    }

    // Update header
    document.getElementById('battalion-title').innerHTML = `<i class="fas fa-shield-alt"></i> ${battalion.name}`;
    document.getElementById('battalion-subtitle').textContent = `APSP - ${battalion.location}`;
    document.title = `${battalion.name} - APSP`;

    // Load battalion image
    const imageSection = document.getElementById('battalion-image');
    imageSection.innerHTML = `
        <img src="${battalion.image}" alt="${battalion.name}" 
             onerror="this.style.display='none'; this.parentElement.innerHTML='<div class=\\'banner-placeholder\\'><div class=\\'battalion-emblem\\'><i class=\\'fas fa-shield-alt\\'></i></div><div class=\\'banner-text\\'><h2>${battalion.name}</h2><p>APSP - ${battalion.location}</p></div></div>'">
    `;

    // Load commandant info
    const commandantSection = document.getElementById('commandant-info');
    
    // Commandant with image
    const commandantHTML = `
        <div class="commandant-header">
            <div class="commandant-image">
                <img src="${battalion.commandantImage || 'images/commandants/default-commandant.jpg'}" alt="${battalion.commandant}"
                     onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22250%22%3E%3Crect fill=%22%23003d82%22 width=%22200%22 height=%22250%22/%3E%3Ccircle cx=%22100%22 cy=%2280%22 r=%2240%22 fill=%22%23ffffff%22 opacity=%220.3%22/%3E%3Crect x=%2260%22 y=%22140%22 width=%2280%22 height=%2290%22 rx=%2210%22 fill=%22%23ffffff%22 opacity=%220.3%22/%3E%3C/svg%3E'">
            </div>
            <div class="commandant-details">
                <div class="commandant-rank">${battalion.designation || 'Commandant'}</div>
                <div class="commandant-name">${battalion.commandant}</div>
                <div class="commandant-battalion">${battalion.name} - ${battalion.location}</div>
            </div>
        </div>
    `;
    
    // Officers grid
    let officersHTML = '';
    battalion.officers.forEach(officer => {
        officersHTML += `
            <div class="officer-card">
                <div class="officer-rank">${officer.rank}</div>
                <div class="officer-name">${officer.name}</div>
            </div>
        `;
    });

    commandantSection.innerHTML = `
        ${commandantHTML}
        <div class="officers-details-section">
            <h2><i class="fas fa-users"></i> Officers Details</h2>
            <div class="officer-grid">
                ${officersHTML}
            </div>
        </div>
        <div class="history-button-section">
            <button class="btn-history" onclick="openHistory()"><i class="fas fa-book"></i> Battalion History</button>
        </div>
    `;

    // Load organizational structure
    const structureSection = document.getElementById('structure-info');
    let groupsHTML = '';

    for (const [groupName, items] of Object.entries(battalion.companies)) {
        let tableRows = '';
        
        items.forEach(item => {
            if (item.office) {
                tableRows += `
                    <tr>
                        <td class="office-name">${item.office}</td>
                        <td>${item.incharge}</td>
                    </tr>
                `;
            } else if (item.company) {
                tableRows += `
                    <tr>
                        <td class="company-name">${item.company}</td>
                        <td>${item.incharge}</td>
                    </tr>
                `;
            }
        });

        groupsHTML += `
            <div class="group-section">
                <h3><i class="fas fa-sitemap"></i> ${groupName}</h3>
                <div class="company-table">
                    <table>
                        <thead>
                            <tr>
                                <th>${groupName === 'Group Head' ? 'Office' : 'Company'}</th>
                                <th>In-Charge</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${tableRows}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    structureSection.innerHTML = `
        <h2><i class="fas fa-layer-group"></i> Organizational Structure</h2>
        ${groupsHTML}
    `;
}

// Open history modal
function openHistory() {
    const battalionId = getBattalionId();
    const battalion = battalionData[battalionId];
    
    if (!battalion) return;
    
    const modal = document.createElement('div');
    modal.className = 'history-modal';
    modal.innerHTML = `
        <div class="history-modal-content">
            <div class="history-modal-header">
                <h2><i class="fas fa-book"></i> ${battalion.name} - History</h2>
                <button class="close-modal" onclick="closeHistory()"><i class="fas fa-times"></i></button>
            </div>
            <div class="history-modal-body">
                <p>${battalion.history || 'History information will be updated soon.'}</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    setTimeout(() => modal.classList.add('active'), 10);
}

// Close history modal
function closeHistory() {
    const modal = document.querySelector('.history-modal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => modal.remove(), 300);
    }
}

// Load details when page loads
window.addEventListener('DOMContentLoaded', loadBattalionDetails);