// TODO this entire file is a stop gap to get these constants out of the PositionDialog
// Todo adding 'Const' to the end of their name to further show that these are not intended to be permanent


export interface TileMetaHeader {
    text: string;
    value: string;
    sortable: boolean;
}

// todo better name?
export const tileMetaHeadersConst: TileMetaHeader[] = [
    { text: 'No', value: 'no', sortable: false },
    { text: 'FileName', value: 'filename', sortable: false },
    { text: 'Series', value: 'series', sortable: false },
    { text: 'Frame', value: 'frame', sortable: false },
    { text: 'C', value: 'c', sortable: false },
    { text: 'SizeC', value: 'size_c', sortable: false },
    { text: 'SizeT', value: 'size_t', sortable: false },
    { text: 'SizeX', value: 'size_x', sortable: false },
    { text: 'SizeY', value: 'size_y', sortable: false },
    { text: 'SizeZ', value: 'size_z', sortable: false }
]


// todo delete this monstrosity...this appears to just be a way to trick someone into thinking they made a functioning auto name pattern finder
export const tileNamePatternsConst = [
    { label: 'Series', text: '', start: 0, end: 17, color: 'success' },
    { label: 'Row', text: '', start: 24, end: 25, color: 'primary' },
    { label: 'Column', text: '', start: 25, end: 27, color: 'deep-orange' },
    { label: 'Field', text: '', start: 27, end: 30, color: 'warning' },
    { label: 'Channel', text: '', start: 30, end: 32, color: 'purple' },
    { label: 'Z Position', text: '', start: 22, end: 23, color: 'blue-grey' },
    { label: 'Time Point', text: '', start: 18, end: 21, color: 'error' }
];

export const nameTypeTableHeaders = [
    { text: 'No', value: 'no' },
    { text: 'FileName', value: 'filename' },
    { text: 'Series', value: 'series' },
    { text: 'Row', value: 'row' },
    { text: 'Column', value: 'col' },
    { text: 'Field', value: 'field' },
    { text: 'Channel', value: 'channel' },
    { text: 'Z Position', value: 'z' },
    { text: 'Time Point', value: 'timeline' }
];
