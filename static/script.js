class Band {
  constructor(name, genre, members, album, songs, userID) {
    this.name = name;
    this.genre = genre;
    this.members = members;
    this.album = album;
    this.songs = songs;
    this.userID = userID;
  }
}
class Model {
  constructor() {
    this.$genreInput = $("#genre-input");
    this.$themeInput = $("#theme-input");
    this.$addInput = $("#additional-input");
    this.$form = $("#band-form");
  }

  async getGenre() {
    const genreID = this.$genreInput.val();
    const resp = await axios.get(`/api/genre/${genreID}`);
    const genre = resp.data.genre;
    return genre;
  }

  async generateBand() {
    const theme = this.$themeInput.val();
    const genre = this.$genreInput.val();
    const resp = await axios.get(`/api/bands/generate/${theme}/${genre}`);
    const band = resp.data;
    return band;
  }

  async generateBandImg(band) {
    const response = await axios.get(
      `/api/bands/generate-img/${band.theme}/${band.genre}/${band.name}`
    );
    const bandImg = response.data;
    return bandImg;
  }
  async generateAlbumArt(band) {
    const response = await axios.get(
      `/api/bands/generate-album-art/${band.theme}/${band.genre}/${band.name}`
    );
    const albumArt = response.data;
    return albumArt;
  }
}

class View {
  constructor() {
    this.$collapse = $("#genre-collapse");
    this.$genreDescription = $("#genre-description");
    this.$modalBtn = $("#modal-btn");
    this.$closeCanvas = $("#close-canvas");
    this.$modalLabel = $("#band-modalLabel");
    this.$spinner = $("#spinner");
    this.$modalContent = $("#modal-content");
  }

  updateDescription(description) {
    this.$genreDescription.text(description);
  }

  triggerModal() {}
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
  }

  async handleSubmit(e) {
    e.preventDefault();
    this.view.$modalBtn.click();
    const band = await this.model.generateBand();
    //const bandImg = this.model.generateBandImg();
  }

  async handleGenreDescription() {
    const genre = await this.model.getGenre();
    this.view.updateDescription(genre.description);
  }
}

new Controller(new View(), new Model());
