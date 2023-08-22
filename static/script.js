class Band {
  constructor(band) {
    this.name = band.name;
    this.bio = band.bio;
    this.genre;
    this.theme;
    this.members = band.members;
    this.albums;
    this.photo;
    this.prompt;
  }
}

class Member {
  constructor(member) {
    this.name = member.name;
    this.role = member.role;
  }
}

class Album {
  constructor(album) {
    this.title = album.title;
    this.songs = album.songs;
    this.albumArt;
  }
}

class Song {
  constructor(song) {
    this.title = song.title;
    this.duration_seconds = song.duration_seconds;
  }
}
class Model {
  constructor() {
    this.$genreInput = $("#genre-input");
    this.$themeInput = $("#theme-input");
    this.$addInput = $("#add-prompt-input");
    this.$form = $("#band-form");
    this.baseApiUrl = "/api/generate";
    this.currBand;
    this.currTheme;
    this.currGenre;
    this.currPrompt;
  }

  clearForm() {
    this.$genreInput.val("");
    this.$themeInput.val("");
    this.$addInput.val("");
  }

  updatePromptValues() {
    this.currTheme = this.$themeInput.val();
    this.currGenre = this.$genreInput.val();
    this.currPrompt = this.$addInput.val() ? this.$addInput.val() : "no text";
  }

  updateCurrBand(band) {
    this.currBand = band;
  }

  async getGenre() {
    const genre = this.$genreInput.val();
    const resp = await axios.get(`/api/genre/${genre}`);
    return resp.data.genre;
  }

  async generateBandData() {
    const resp = await axios.get(
      `${this.baseApiUrl}/band-data/${this.currTheme}/${this.currGenre}/${this.currPrompt}`
    );
    const bandData = resp.data;
    return bandData.data;
  }

  async generatephoto(band) {
    const response = await axios.get(
      `${this.baseApiUrl}/img/${this.currTheme}/${this.currGenre}/${band.members.length}/${this.currPrompt}`
    );
    const photoUrl = response.data;
    return photoUrl.image;
  }

  async generateAlbumArt(band, album) {
    const response = await axios.get(
      `${this.baseApiUrl}/album-art/${this.currTheme}/${this.currGenre}/${band.name}/${album.title}/test`
    );
    const albumArt = response.data;
    return albumArt.image;
  }
  makeBand(bandData, photo, albumArt) {
    const band = new Band(bandData);
    band.photo = photo;
    band.genre = this.currGenre;
    band.theme = this.currTheme;
    band.prompt = this.currPrompt;
    const album = this.makeAlbum(bandData.albums[0], albumArt);
    band.albums = [album];
    band.members = band.members.map((member) => {
      return new Member(member);
    });
    return band;
  }

  makeAlbum(albumData, albumArt) {
    const album = new Album(albumData);
    album.albumArt = albumArt;
    album.songs = albumData.songs.map((song) => {
      return new Song(song);
    });
    return album;
  }
  async saveAndReturnBand() {
    const resp = await axios.post("/api/band", this.currBand);
    const band = resp.data.band;
    return band;
  }

  resetCurrentVallues() {
    this.currBand = null;
    this.currTheme = null;
    this.currGenre = null;
    this.currPrompt = null;
  }
}

class View {
  constructor() {
    this.$collapse = $("#genre-collapse");
    this.$genreDescription = $("#genre-description");
    this.$modalBtn = $("#modal-btn");
    this.$closeModalBtm = $("#close-modal");
    this.$closeCanvas = $("#close-canvas");
    this.$modalLabel = $("#band-modalLabel");
    this.$spinner = $("#spinner");
    this.$modalContent = $("#modal-content");
    this.$status = $("#status");
    this.$saveBtn = $("#save-btn");
    this.$reGenBtn = $("#re-gen-btn");
    this.$discardBtn = $("#discard-btn");
    this.$backBtn = $("#back-btn");
    this.$bandList = $("#band-list");
    this.$errorReTryBtn = $("#error-retry-btn");
  }

  updateDescription(description) {
    this.$genreDescription.text(description);
  }

  renderSavedBand(band) {
    return;
  }

  toggleButtons() {
    this.$saveBtn.prop("disabled", (i, v) => !v);
    this.$reGenBtn.prop("disabled", (i, v) => !v);
    this.$discardBtn.prop("disabled", (i, v) => !v);
    this.$backBtn.prop("disabled", (i, v) => !v);
  }

  toggleSpinner() {
    this.$spinner.toggle();
  }

  resetModal() {
    this.$modalContent.empty();
  }

  closeModal() {
    this.$closeModalBtm.click();
  }

  updateStatus(step) {
    if (step === 1) {
      this.$status.text("Generating Band Data...");
    } else if (step === 2) {
      this.$status.text("Generating Band Image...");
    } else if (step === 3) {
      this.$status.text("Generating Album Art...");
    } else if (step === 4) {
      this.$status.text("Review");
    } else {
      this.$status.text("Oopsies! Something went wrong.");
    }
  }

  modalError(err) {
    this.$modalContent.empty();
    this.$errorReTryBtn.show();
    this.$modalContent.append(`
    <div class="alert alert-danger" role="alert">
    ${err}</div>
    <p>Something went wrong! Please try again.</p>`);
  }

  renderBandReview(band) {
    this.$modalLabel.text(band.name);
    this.$modalContent.empty();
    this.$modalContent.append(`
    <div class="row">
    <div class="col-6">
    <img src="data:image/png;base64,${
      band.photo
    }" alt="img_data"  class="img-fluid" id="imgslot"/>
    </div>
    <div class="col-6">
      <h3>Band Bio</h3>
      <p>${band.bio}</p>
      <h3>Members</h3>
      <ul>
        ${band.members
          .map((member) => {
            return `<li>${member.name} : ${member.role}</li>`;
          })
          .join("")}
      </ul>
      <h3>Albums</h3>
      <img src="data:image/png;base64,${
        band.albums[0].albumArt
      }" class="img-fluid" alt="Responsive image">
      <ul>
        ${band.albums.map((album) => {
          return `<li>${album.title}</li>
          <ul>${album.songs.map((song) => {
            return `<li>${song.title} : ${song.duration_seconds}</li>`;
          })} </ul>`;
        })}
          </ul>
    </div>`);
  }
}
class Controller {
  constructor(view, model) {
    this.view = view;
    this.model = model;
    this.handleGenreDescription();
    this.model.$form.on("submit", async (e) => {
      this.handleSubmit(e);
    });
    this.model.$genreInput.on("change", async () =>
      this.handleGenreDescription()
    );
    this.view.$saveBtn.on("click", async () => this.handleSave());
    this.view.$reGenBtn.on("click", async () => this.handleReGen());
    this.view.$discardBtn.on("click", async () => this.handleDiscard());
    this.view.$backBtn.on("click", async () => this.handleBack());
    this.view.$errorReTryBtn.on("click", async () => this.handleReGen());
    // this.view.$bandsArea.on("click", ".band-card", async (e) =>
    //   this.handleBandCardClick(e)
    // );
  }

  async handleSave() {
    const band = await this.model.saveAndReturnBand();
    this.view.closeModal();
    this.view.toggleButtons();
    this.view.resetModal();
    this.model.clearForm();
    this.model.resetCurrentVallues();
    this.view.renderSavedBand(band);
  }

  handleReGen() {
    this.view.toggleButtons();
    this.view.resetModal();
    this.handleGenerateBand();
  }

  handleDiscard() {
    this.model.clearForm();
    this.model.resetCurrentVallues();
    this.view.closeModal();
    this.view.toggleButtons();
    this.view.resetModal();
  }

  async handleSubmit(e) {
    e.preventDefault();
    this.model.updatePromptValues();
    this.view.$closeCanvas.click();
    this.view.$modalBtn.click();
    this.handleGenerateBand();
  }

  async handleGenerateBand() {
    this.view.$errorReTryBtn.hide();
    this.view.toggleSpinner();
    let step = 1;
    this.view.updateStatus(step);
    try {
      const bandData = await this.model.generateBandData();
      step++;
      this.view.updateStatus(step);
      const photoUrl = await this.model.generatephoto(bandData);
      step++;
      this.view.updateStatus(step);
      const albumArt = await this.model.generateAlbumArt(
        bandData,
        bandData.albums[0]
      );
      step++;
      this.view.updateStatus(step);
      const band = this.model.makeBand(bandData, photoUrl, albumArt);
      this.model.updateCurrBand(band);
      this.view.toggleSpinner();
      this.view.renderBandReview(this.model.currBand);
      this.view.toggleButtons();
    } catch (err) {
      this.handleError(err);
    }
  }

  handleError(err) {
    const step = 0;
    this.view.toggleSpinner();
    this.view.$errorReTryBtn.show();
    this.view.updateStatus(step);
    this.view.modalError(err);
  }

  async handleGenreDescription() {
    const genre = await this.model.getGenre();
    this.view.updateDescription(genre.description);
  }
}

if ($("#band-form").length > 0) {
  new Controller(new View(), new Model());
}
