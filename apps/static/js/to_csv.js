const output = () => {
  const table = document.getElementById('mytable')
  const escaped = /,|\r?\n|\r|"/;
  const e = /"/g;
  const bom = new Uint8Array([0xEF, 0xBB, 0xBF])
  const csv = []
  const row = []

  for (let r = 0; r < table.rows.length; r++) {
    row.length = 0
    for (let c = 0; c < table.rows[r].cells.length; c++) {
      const field = table.rows[r].cells[c].textContent
      row.push(escaped.test(field) ? '"' + field.replace(e, '""') + '"' : field)
    }
    csv.push(row.join(','))
  }

  const blob = new Blob([bom, csv.join('\n')], {
    'type': 'text/csv'
  })

  const a = document.getElementById('output_btn')

  a.download = 'mytable.csv'

  a.href = window.URL.createObjectURL(blob)

}
