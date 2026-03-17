// Node.js ESModule strict - need dynamic import and top-level await if type:module
import fs from 'fs';
import readline from 'readline';

// Import as dynamic require for .json
const allStatements = JSON.parse(fs.readFileSync('./all_words_with_statements.json', 'utf8'));
let acceptedStatements = [];
let rejectedStatements = [];
try {
    acceptedStatements = JSON.parse(fs.readFileSync('./accepted_statements.json', 'utf8'));
    rejectedStatements = JSON.parse(fs.readFileSync('./rejected_statements.json', 'utf8'));
} catch (e) {
    acceptedStatements = [];
    rejectedStatements = [];
}

const filteredStatements = allStatements.filter(item =>
    item.statement &&
    (
        // item.statement.toLowerCase().includes('innocent')// ||
        item.statement.toLowerCase().includes('did not') ||
        item.statement.toLowerCase().includes('guilty') ||
        item.statement.toLowerCase().includes("didn't")
    )
);

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function checkForDuplicate(statement) {
    return acceptedStatements.some(item =>
        item.firstName === statement.firstName &&
        item.lastName === statement.lastName
    ) || rejectedStatements.some(item =>
        item.firstName === statement.firstName &&
        item.lastName === statement.lastName
    );
}

function saveAcceptedStatements() {
    fs.writeFileSync('./accepted_statements.json', JSON.stringify(acceptedStatements, null, 2));
}

function saveRejectedStatements() {
    fs.writeFileSync('./rejected_statements.json', JSON.stringify(rejectedStatements, null, 2));
}
let index = 0;

function askNext() {
    // Skip duplicates
    while (index < filteredStatements.length && checkForDuplicate(filteredStatements[index])) {
        index++;
    }

    if (index >= filteredStatements.length) {
        console.log('No more statements to review.');
        rl.close();
        return;
    }

    const statement = filteredStatements[index];
    console.log('\n-------');
    console.log(`Name: ${statement.firstName} ${statement.lastName}`);
    console.log(`Statement:\n${statement.statement}`);
    rl.question('Accept this statement? ("l" for accept, "a" for reject, anything else to quit): ', answer => {
        if (answer.toLowerCase() === 'l') {
            acceptedStatements.push(statement);
            saveAcceptedStatements();
            console.log('Accepted.');
        } else if (answer.toLowerCase() === 'a') {
            rejectedStatements.push(statement);
            saveRejectedStatements();
            console.log('Rejected.');
        } else {
            console.log('Exiting.');
            rl.close();
            return;
        }        index++;
        askNext();
    });
}

askNext();
