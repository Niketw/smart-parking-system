import { useEffect, useMemo, useState } from 'react'
import './App.css'
import { api } from './api'

function TextInput({ label, value, onChange, placeholder }) {
  return (
    <label style={{ display: 'block', marginBottom: 8 }}>
      <div style={{ fontSize: 12, marginBottom: 4 }}>{label}</div>
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        style={{ width: '100%', padding: 8 }}
      />
    </label>
  )
}

function TicketForm({ onCreated }) {
  const [ticketNumber, setTicketNumber] = useState('')
  const [licensePlate, setLicensePlate] = useState('')
  const [vehicleMake, setVehicleMake] = useState('')
  const [vehicleModel, setVehicleModel] = useState('')
  const [parkingSpot, setParkingSpot] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      const payload = {
        ticketNumber: ticketNumber.trim(),
        licensePlate: licensePlate.trim(),
        vehicleMake: vehicleMake.trim() || undefined,
        vehicleModel: vehicleModel.trim() || undefined,
        parkingSpot: parkingSpot.trim(),
      }
      await api.createTicket(payload)
      setTicketNumber('')
      setLicensePlate('')
      setVehicleMake('')
      setVehicleModel('')
      setParkingSpot('')
      onCreated?.()
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8 }}>
      <h2 style={{ marginTop: 0 }}>Create Parking Ticket</h2>
      <TextInput label="Ticket Number" value={ticketNumber} onChange={setTicketNumber} placeholder="A12345" />
      <TextInput label="License Plate" value={licensePlate} onChange={setLicensePlate} placeholder="ABC123" />
      <TextInput label="Vehicle Make" value={vehicleMake} onChange={setVehicleMake} placeholder="Toyota" />
      <TextInput label="Vehicle Model" value={vehicleModel} onChange={setVehicleModel} placeholder="Corolla" />
      <TextInput label="Parking Spot" value={parkingSpot} onChange={setParkingSpot} placeholder="P-12" />
      {error && <div style={{ color: 'red', marginBottom: 8 }}>{error}</div>}
      <button type="submit" disabled={submitting || !ticketNumber || !licensePlate || !parkingSpot}>
        {submitting ? 'Saving...' : 'Create Ticket'}
      </button>
    </form>
  )
}

function TicketsList() {
  const [tickets, setTickets] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')
  const [showActiveOnly, setShowActiveOnly] = useState(true)

  const filtered = useMemo(() => tickets, [tickets])

  async function loadTickets() {
    setLoading(true)
    setError('')
    try {
      const data = showActiveOnly ? await api.listTickets({ isActive: true }) : await api.listTickets()
      setTickets(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function doSearch() {
    if (!query.trim()) {
      return loadTickets()
    }
    setLoading(true)
    setError('')
    try {
      const data = await api.searchTickets(query.trim())
      setTickets(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function checkout(id) {
    try {
      await api.checkoutTicket(id)
      await loadTickets()
    } catch (err) {
      alert(err.message)
    }
  }

  useEffect(() => {
    loadTickets()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showActiveOnly])

  return (
    <div style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8 }}>
      <h2 style={{ marginTop: 0 }}>Tickets</h2>
      <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search by ticket/plate/spot" style={{ flex: 1, padding: 8 }} />
        <button onClick={doSearch} disabled={loading}>Search</button>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <input type="checkbox" checked={showActiveOnly} onChange={(e) => setShowActiveOnly(e.target.checked)} />
          Active only
        </label>
        <button onClick={loadTickets} disabled={loading}>Refresh</button>
      </div>
      {error && <div style={{ color: 'red', marginBottom: 8 }}>{error}</div>}
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc', padding: 8 }}>Ticket</th>
                <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc', padding: 8 }}>Plate</th>
                <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc', padding: 8 }}>Vehicle</th>
                <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc', padding: 8 }}>Spot</th>
                <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc', padding: 8 }}>Check-in</th>
                <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc', padding: 8 }}>Check-out</th>
                <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc', padding: 8 }}>Active</th>
                <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc', padding: 8 }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((t) => (
                <tr key={t.id}>
                  <td style={{ padding: 8 }}>{t.ticketNumber}</td>
                  <td style={{ padding: 8 }}>{t.licensePlate}</td>
                  <td style={{ padding: 8 }}>{[t.vehicleMake, t.vehicleModel].filter(Boolean).join(' ') || '-'}</td>
                  <td style={{ padding: 8 }}>{t.parkingSpot}</td>
                  <td style={{ padding: 8 }}>{t.checkInTime ? new Date(t.checkInTime).toLocaleString() : '-'}</td>
                  <td style={{ padding: 8 }}>{t.checkOutTime ? new Date(t.checkOutTime).toLocaleString() : '-'}</td>
                  <td style={{ padding: 8 }}>{t.isActive ? 'Yes' : 'No'}</td>
                  <td style={{ padding: 8 }}>
                    {t.isActive ? (
                      <button onClick={() => checkout(t.id)}>Checkout</button>
                    ) : (
                      <span>-</span>
                    )}
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={8} style={{ padding: 8, textAlign: 'center' }}>No tickets</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

function App() {
  const [reloadKey, setReloadKey] = useState(0)
  return (
    <div style={{ maxWidth: 960, margin: '0 auto', padding: 16 }}>
      <h1>Smart Parking System</h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 16 }}>
        <TicketForm onCreated={() => setReloadKey((k) => k + 1)} />
        {/* Changing key forces list to reload via effect */}
        <div key={reloadKey}>
          <TicketsList />
        </div>
      </div>
    </div>
  )
}

export default App
