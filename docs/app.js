const samples = [
  { id: "internet", type: "bill", label: "Bill", name: "Home internet", provider: "Kifaru Fibre", days: 8, amount: "KES 4,250", amountNote: "monthly", file: "kifaru-fibre-invoice.pdf", evidence: (date) => `“Please pay KES 4,250 on or before ${date} to avoid interruption of service.”`, match: "bill invoice home internet broadband due payment renewal" },
  { id: "laptop", type: "warranty", label: "Warranty", name: "Laptop coverage", provider: "Tendaji Computers", days: 19, amount: null, amountNote: "", file: "tendaji-laptop-warranty.pdf", evidence: (date) => `“Limited warranty coverage for this device expires on ${date}.”`, match: "warranty laptop coverage expiry expiration device" },
  { id: "design", type: "subscription", label: "Subscription", name: "Design suite", provider: "PixelDesk Studio", days: 25, amount: "USD 18.00", amountNote: "monthly", file: "pixeldesk-renewal-notice.txt", evidence: (date) => `“Your PixelDesk Studio plan renews on ${date}. Your monthly charge will be USD 18.00.”`, match: "subscription software design suite renew renewal plan" },
  { id: "insurance", type: "insurance", label: "Insurance", name: "Home cover", provider: "Jirani Assurance", days: 42, amount: "KES 17,800", amountNote: "annual premium", file: "jirani-home-policy.pdf", evidence: (date) => `“Policy period ends ${date}. Renew before the end date to maintain cover.”`, match: "insurance policy home cover premium renewal" },
  { id: "kettle", type: "warranty", label: "Warranty", name: "Kitchen appliance", provider: "Nyota Home Store", days: -3, amount: null, amountNote: "", file: "nyota-kettle-receipt.pdf", evidence: (date) => `“Warranty valid until ${date}, subject to the terms printed on this receipt.”`, match: "warranty kettle kitchen appliance receipt expires expired" },
];

const state = { range: 30, category: "all", query: "" };
const results = document.querySelector("#results");
const emptyState = document.querySelector("#empty-state");
const searchInput = document.querySelector("#search");
const clearSearch = document.querySelector("#clear-search");
const dialog = document.querySelector("#evidence-dialog");
const formatDate = (value) => new Intl.DateTimeFormat("en", { day: "numeric", month: "short", year: "numeric" }).format(value);
const dueDate = (offset) => { const d = new Date(); d.setHours(12, 0, 0, 0); d.setDate(d.getDate() + offset); return d; };
const countdown = (days) => days < 0 ? `${Math.abs(days)} days overdue` : days === 0 ? "Due today" : `In ${days} days`;

function render() {
  const q = state.query.trim().toLowerCase();
  const visible = samples.filter((item) => {
    const inRange = state.range === "all" || (item.days >= -30 && item.days <= Number(state.range));
    const categoryMatch = state.category === "all" || item.type === state.category;
    const queryMatch = !q || `${item.name} ${item.provider} ${item.label} ${item.file} ${item.match}`.toLowerCase().includes(q);
    return inRange && categoryMatch && queryMatch;
  }).sort((a, b) => a.days - b.days);

  document.querySelector("#range-caption").textContent = state.range === "all" ? "All sample dates" : `Due or expiring in the next ${state.range} days`;
  document.querySelector("#all-count").textContent = samples.length;
  clearSearch.hidden = !state.query;
  emptyState.hidden = visible.length > 0;
  results.innerHTML = visible.map((item) => {
    const date = dueDate(item.days);
    const dateLabel = formatDate(date);
    const amount = item.amount ? `<div class="amount-cell"><strong>${item.amount}</strong><small>${item.amountNote}</small></div>` : `<div class="amount-cell"><strong class="muted">—</strong><small>Not listed</small></div>`;
    const statusClass = item.days < 0 ? "overdue" : "";
    return `<article class="record-row"><div class="item-cell"><span class="type-icon ${item.type}">${item.label[0]}</span><span class="item-copy"><strong>${item.name}</strong><small>${item.provider} · ${item.label}</small></span></div><div class="date-cell"><strong>${dateLabel}</strong><small class="${statusClass}">${countdown(item.days)}</small></div>${amount}<button class="evidence-button" type="button" data-evidence="${item.id}">Review evidence <span aria-hidden="true">↗</span></button></article>`;
  }).join("");
}

document.querySelectorAll(".range-tab").forEach((button) => button.addEventListener("click", () => {
  state.range = button.dataset.range;
  document.querySelectorAll(".range-tab").forEach((tab) => tab.classList.toggle("is-active", tab === button));
  render();
}));
document.querySelectorAll(".category-chip").forEach((button) => button.addEventListener("click", () => {
  state.category = button.dataset.category;
  document.querySelectorAll(".category-chip").forEach((chip) => chip.classList.toggle("is-active", chip === button));
  render();
}));
searchInput.addEventListener("input", () => { state.query = searchInput.value; render(); });
clearSearch.addEventListener("click", () => { searchInput.value = ""; state.query = ""; searchInput.focus(); render(); });
document.querySelector("#reset-filters").addEventListener("click", () => {
  state.range = 30; state.category = "all"; state.query = ""; searchInput.value = "";
  document.querySelectorAll(".range-tab").forEach((tab) => tab.classList.toggle("is-active", tab.dataset.range === "30"));
  document.querySelectorAll(".category-chip").forEach((chip) => chip.classList.toggle("is-active", chip.dataset.category === "all"));
  render();
});
results.addEventListener("click", (event) => {
  const button = event.target.closest("[data-evidence]");
  if (!button) return;
  const item = samples.find((entry) => entry.id === button.dataset.evidence);
  if (!item) return;
  const date = formatDate(dueDate(item.days));
  document.querySelector("#dialog-title").textContent = `${item.label} · ${item.name}`;
  document.querySelector("#dialog-subtitle").textContent = `${item.provider} · ${date} · ${countdown(item.days)}`;
  document.querySelector("#dialog-evidence").textContent = item.evidence(date);
  document.querySelector("#dialog-file-name").textContent = item.file;
  dialog.showModal();
});
render();
