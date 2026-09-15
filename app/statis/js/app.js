const $ = id => document.getElementById(id);

const el = {
    formPeriksa: $("form-periksa"),
    periksaKaryawan: $("periksa-karyawan"),
    periksaTanggal: $("periksa-tanggal"),
    hasilPeriksa: $("hasil-periksa"),
    formJadwal: $("form-jadwal"),
    kodeKaryawan: $("kode-karyawan"),
    tanggalMulai: $("tanggal-mulai"),
    tanggalSelesai: $("tanggal-selesai"),
    pesan: $("pesan"),
    jumlahKaryawan: $("jumlah-karyawan"),
    jumlahHari: $("jumlah-hari"),
    periode: $("periode"),
    wadahTabel: $("wadah-tabel"),
    eksporCsv: $("ekspor-csv"),
    eksporExcel: $("ekspor-excel")
};

const namaShift = { P:"Pagi", S:"Siang", M:"Malam", L:"Libur" };

function normalisasiShift(nilai) {
    if (nilai == null) return "-";
    if (typeof nilai !== "object") return String(nilai).trim().toUpperCase();

    const shift = nilai.kode ?? nilai.kode_shift ?? nilai.shift ??
        nilai.status ?? nilai.nama_shift ?? nilai.nama ?? "-";

    return typeof shift === "string" ? shift.trim().toUpperCase() : String(shift);
}

function kelasShift(shift) {
    const kode = normalisasiShift(shift).toLowerCase();
    return ["p","s","m","l"].includes(kode) ? `shift-${kode}` : "";
}

function formatTanggal(tanggal, pendek = false) {
    if (!tanggal || tanggal === "-") return "-";
    const date = new Date(`${tanggal}T00:00:00`);
    if (Number.isNaN(date.getTime())) return tanggal;

    return new Intl.DateTimeFormat("id-ID", {
        day:"2-digit",
        month:pendek ? "2-digit" : "long",
        year:pendek ? undefined : "numeric"
    }).format(date);
}

function daftarTanggal(mulai, selesai) {
    const hasil = [];
    const tanggal = new Date(`${mulai}T00:00:00`);
    const akhir = new Date(`${selesai}T00:00:00`);

    while (tanggal <= akhir) {
        const y = tanggal.getFullYear();
        const m = String(tanggal.getMonth() + 1).padStart(2, "0");
        const d = String(tanggal.getDate()).padStart(2, "0");
        hasil.push(`${y}-${m}-${d}`);
        tanggal.setDate(tanggal.getDate() + 1);
    }

    return hasil;
}

function tampilkanPesan(teks, tipe = "error") {
    el.pesan.textContent = teks;
    el.pesan.className = `pesan pesan-${tipe}`;
}

function sembunyikanPesan() {
    el.pesan.className = "pesan tersembunyi";
}

async function ambilJson(url) {
    const respons = await fetch(url);
    const data = await respons.json();

    if (!respons.ok) {
        throw new Error(data.pesan || data.detail || "Terjadi kesalahan pada permintaan.");
    }

    return data;
}

async function muatKaryawan() {
    try {
        const respons = await ambilJson("/api/v1/karyawan");
        const daftar = respons.data || [];

        el.periksaKaryawan.innerHTML = '<option value="">Semua Karyawan</option>';
        el.kodeKaryawan.innerHTML = '<option value="">Semua Karyawan</option>';

        daftar.forEach(karyawan => {
            const teks = `${karyawan.kode_karyawan} · ${karyawan.nama}`;
            el.periksaKaryawan.add(new Option(teks, karyawan.kode_karyawan));
            el.kodeKaryawan.add(new Option(teks, karyawan.kode_karyawan));
        });
    } catch (error) {
        tampilkanPesan(error.message);
    }
}

function normalisasiJadwal(karyawan) {
    const sumber = karyawan.jadwal ?? karyawan.daftar_jadwal ??
        karyawan.detail_jadwal ?? [];

    if (Array.isArray(sumber)) {
        return Object.fromEntries(
            sumber
                .filter(item => item?.tanggal)
                .map(item => [
                    item.tanggal,
                    normalisasiShift(
                        item.shift ?? item.kode_shift ?? item.status ?? item
                    )
                ])
        );
    }

    if (sumber && typeof sumber === "object") {
        return Object.fromEntries(
            Object.entries(sumber).map(([tanggal, shift]) => [
                tanggal,
                normalisasiShift(shift)
            ])
        );
    }

    return {};
}

function ambilNilaiPeriksa(respons) {
    const data = respons.data || respons;
    const karyawan = data.karyawan || {};

    return {
        kode: data.kode_karyawan ?? karyawan.kode_karyawan ?? "-",
        nama: data.nama ?? karyawan.nama ?? "-",
        tanggal: data.tanggal ?? data.jadwal?.tanggal ?? "-",
        shift: normalisasiShift(
            data.shift ??
            data.kode_shift ??
            data.status ??
            data.jadwal?.shift ??
            data.jadwal?.kode_shift ??
            data.jadwal
        )
    };
}

function renderHasilPeriksa(data, tanggal) {
    const baris = data.map(karyawan => {
        const shift = normalisasiShift(karyawan.shift);

        return `
            <tr>
                <td>${karyawan.kode_karyawan ?? "-"}</td>
                <td class="nama-karyawan">${karyawan.nama ?? "-"}</td>
                <td><span class="badge ${kelasShift(shift)}">${shift}</span></td>
                <td>${namaShift[shift] || shift}</td>
            </tr>
        `;
    }).join("");

    el.hasilPeriksa.innerHTML = `
        <div class="hasil-periksa-header">
            <div>
                <h3>Hasil Cek Shift</h3>
                <p>${formatTanggal(tanggal)}</p>
            </div>
            <span class="jumlah-hasil">${data.length} Karyawan</span>
        </div>
        <div class="wadah-tabel">
            <table class="tabel-jadwal tabel-periksa">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nama Karyawan</th>
                        <th>Shift</th>
                        <th>Keterangan</th>
                    </tr>
                </thead>
                <tbody>${baris}</tbody>
            </table>
        </div>
    `;
}

async function periksaSatuKaryawan(kode, tanggal) {
    const parameter = new URLSearchParams({ kode_karyawan:kode, tanggal });
    const respons = await ambilJson(`/api/v1/jadwal/periksa?${parameter}`);
    const hasil = ambilNilaiPeriksa(respons);

    renderHasilPeriksa([{
        kode_karyawan:hasil.kode,
        nama:hasil.nama,
        shift:hasil.shift
    }], tanggal);
}

async function periksaSemuaKaryawan(tanggal) {
    const parameter = new URLSearchParams({
        tanggal_mulai:tanggal,
        tanggal_selesai:tanggal
    });

    const respons = await ambilJson(`/api/v1/jadwal?${parameter}`);
    const data = Array.isArray(respons.data) ? respons.data : [];

    renderHasilPeriksa(data.map(karyawan => ({
        kode_karyawan:karyawan.kode_karyawan,
        nama:karyawan.nama,
        shift:normalisasiJadwal(karyawan)[tanggal]
    })), tanggal);
}

el.formPeriksa.addEventListener("submit", async event => {
    event.preventDefault();
    sembunyikanPesan();

    try {
        const kode = el.periksaKaryawan.value;
        const tanggal = el.periksaTanggal.value;

        if (kode) {
            await periksaSatuKaryawan(kode, tanggal);
        } else {
            await periksaSemuaKaryawan(tanggal);
        }

        el.hasilPeriksa.classList.remove("tersembunyi");
    } catch (error) {
        el.hasilPeriksa.classList.add("tersembunyi");
        tampilkanPesan(error.message);
    }
});

function renderTabelJadwal(data, tanggal) {
    const header = tanggal
        .map(item => `<th title="${formatTanggal(item)}">${formatTanggal(item, true)}</th>`)
        .join("");

    const baris = data.map(karyawan => {
        const jadwal = normalisasiJadwal(karyawan);

        const kolom = tanggal.map(item => {
            const shift = normalisasiShift(jadwal[item]);
            return shift === "-"
                ? "<td>-</td>"
                : `<td><span class="badge ${kelasShift(shift)}" title="${namaShift[shift] || shift}">${shift}</span></td>`;
        }).join("");

        return `
            <tr>
                <td>${karyawan.kode_karyawan ?? "-"}</td>
                <td class="nama-karyawan">${karyawan.nama ?? "-"}</td>
                ${kolom}
            </tr>
        `;
    }).join("");

    el.wadahTabel.innerHTML = `
        <table class="tabel-jadwal">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nama Karyawan</th>
                    ${header}
                </tr>
            </thead>
            <tbody>${baris}</tbody>
        </table>
    `;
}

function aturEkspor(aktif) {
    el.eksporCsv.disabled = !aktif;
    el.eksporExcel.disabled = !aktif;
}

el.tanggalMulai.addEventListener("change", () => {
    el.tanggalSelesai.min = el.tanggalMulai.value;
    el.tanggalSelesai.value = el.tanggalMulai.value;
    aturEkspor(false);
});

el.tanggalSelesai.addEventListener("change", () => aturEkspor(false));
el.kodeKaryawan.addEventListener("change", () => aturEkspor(false));

el.formJadwal.addEventListener("submit", async event => {
    event.preventDefault();
    sembunyikanPesan();

    try {
        const kode = el.kodeKaryawan.value;
        const mulai = el.tanggalMulai.value;
        const selesai = el.tanggalSelesai.value;

        if (selesai < mulai) {
            throw new Error("Tanggal selesai tidak boleh sebelum tanggal mulai.");
        }

        const parameter = new URLSearchParams({
            tanggal_mulai:mulai,
            tanggal_selesai:selesai
        });

        if (kode) parameter.set("kode_karyawan", kode);

        const respons = await ambilJson(`/api/v1/jadwal?${parameter}`);
        const data = Array.isArray(respons.data) ? respons.data : [];
        const tanggal = daftarTanggal(mulai, selesai);

        renderTabelJadwal(data, tanggal);

        el.jumlahKaryawan.textContent =
            respons.meta?.jumlah_karyawan ?? data.length;

        el.jumlahHari.textContent =
            respons.meta?.jumlah_hari ?? tanggal.length;

        el.periode.textContent =
            mulai === selesai
                ? formatTanggal(mulai)
                : `${formatTanggal(mulai)} – ${formatTanggal(selesai)}`;

        aturEkspor(true);
    } catch (error) {
        aturEkspor(false);
        tampilkanPesan(error.message);
    }
});

function ekspor(format) {
    const parameter = new URLSearchParams({
        tanggal_mulai:el.tanggalMulai.value,
        tanggal_selesai:el.tanggalSelesai.value,
        format
    });

    if (el.kodeKaryawan.value) {
        parameter.set("kode_karyawan", el.kodeKaryawan.value);
    }

    window.location.href = `/api/v1/jadwal/ekspor?${parameter}`;
}

el.eksporCsv.addEventListener("click", () => ekspor("csv"));
el.eksporExcel.addEventListener("click", () => ekspor("xlsx"));

muatKaryawan();